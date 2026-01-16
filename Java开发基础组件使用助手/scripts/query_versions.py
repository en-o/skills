#!/usr/bin/env python3
"""
JDevelops 组件版本查询工具

用于查询 Maven 仓库上 cn.tannn.jdevelops 组件的最新版本信息
支持多个 Maven 仓库源，自动切换
"""

import requests
import json
import sys
import time
import os
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin


class JDevelopsVersionChecker:
    """JDevelops 版本查询器"""

    # Maven 仓库配置（按优先级排序）
    MAVEN_REPOS = [
        {
            'name': 'Maven Central',
            'search_api': 'https://search.maven.org/solrsearch/select',
            'type': 'maven_central'
        },
        {
            'name': 'Aliyun Maven Mirror',
            'search_api': 'https://maven.aliyun.com/nexus/service/local/lucene/search',
            'type': 'nexus'
        },
    ]

    def __init__(self, verbose: bool = False, proxy: Optional[str] = None):
        """
        初始化版本查询器

        Args:
            verbose: 是否显示详细日志
            proxy: 代理服务器地址，如 'http://127.0.0.1:7890'
        """
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JDevelops-Version-Checker/2.0'
        })

        # 设置代理
        if proxy:
            self.session.proxies.update({
                'http': proxy,
                'https': proxy
            })
            self._log(f"✅ 使用代理: {proxy}")

        # 从环境变量读取代理
        elif os.environ.get('HTTP_PROXY') or os.environ.get('HTTPS_PROXY'):
            http_proxy = os.environ.get('HTTP_PROXY', os.environ.get('http_proxy'))
            https_proxy = os.environ.get('HTTPS_PROXY', os.environ.get('https_proxy'))
            if http_proxy:
                self.session.proxies['http'] = http_proxy
            if https_proxy:
                self.session.proxies['https'] = https_proxy
            self._log(f"✅ 使用环境变量代理")

    def _log(self, message: str, force: bool = False):
        """输出日志"""
        if self.verbose or force:
            print(message, file=sys.stderr)

    def search_group(self, group_id: str = "cn.tannn.jdevelops", rows: int = 100) -> List[Dict]:
        """
        搜索指定 groupId 下的所有组件

        Args:
            group_id: Maven groupId，默认为 cn.tannn.jdevelops
            rows: 返回结果数量，默认 100

        Returns:
            组件列表，每个组件包含 artifactId 和最新版本信息
        """
        self._log(f"🔍 开始查询 groupId: {group_id}")

        # 尝试所有 Maven 仓库
        for repo in self.MAVEN_REPOS:
            self._log(f"📡 尝试仓库: {repo['name']}")

            try:
                result = self._search_group_from_repo(repo, group_id, rows)
                if result:
                    self._log(f"✅ 从 {repo['name']} 查询成功，找到 {len(result)} 个组件", force=True)
                    return result
                else:
                    self._log(f"⚠️  {repo['name']} 未找到结果，尝试下一个仓库")
            except Exception as e:
                self._log(f"❌ {repo['name']} 查询失败: {e}")
                continue

        # 所有仓库都失败
        print("❌ 所有 Maven 仓库都查询失败", file=sys.stderr)
        print("💡 可能的原因:", file=sys.stderr)
        print("   1. 网络连接问题（尝试检查网络或使用代理）", file=sys.stderr)
        print("   2. Maven 仓库暂时不可用", file=sys.stderr)
        print("   3. 组件 groupId 不存在", file=sys.stderr)
        print("\n💡 解决方案:", file=sys.stderr)
        print("   - 使用 -v 参数查看详细日志: python query_versions.py -v", file=sys.stderr)
        print("   - 设置代理: python query_versions.py --proxy http://127.0.0.1:7890", file=sys.stderr)
        print("   - 或设置环境变量: export HTTP_PROXY=http://127.0.0.1:7890", file=sys.stderr)
        return []

    def _search_group_from_repo(self, repo: Dict, group_id: str, rows: int) -> List[Dict]:
        """从指定仓库查询组件组"""
        if repo['type'] == 'maven_central':
            return self._search_maven_central_group(repo['search_api'], group_id, rows)
        elif repo['type'] == 'nexus':
            return self._search_nexus_group(repo['search_api'], group_id, rows)
        return []

    def _search_maven_central_group(self, api_url: str, group_id: str, rows: int) -> List[Dict]:
        """从 Maven Central 查询"""
        params = {
            'q': f'g:{group_id}',
            'rows': rows,
            'wt': 'json',
            'core': 'gav'
        }

        # 重试机制：指数退避
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    wait_time = 2 ** attempt  # 指数退避: 2s, 4s, 8s
                    self._log(f"⏳ 等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    self._log(f"🔄 第 {attempt + 1} 次重试...")

                response = self.session.get(
                    api_url,
                    params=params,
                    timeout=30,
                    verify=True  # 验证 SSL 证书
                )

                self._log(f"📊 HTTP 状态码: {response.status_code}")
                response.raise_for_status()

                data = response.json()
                self._log(f"📦 响应数据大小: {len(json.dumps(data))} 字节")

                # 解析返回结果
                docs = data.get('response', {}).get('docs', [])
                self._log(f"📋 原始结果数量: {len(docs)}")

                # 按 artifactId 分组，获取每个组件的最新版本
                artifacts = {}
                for doc in docs:
                    artifact_id = doc.get('a', '')
                    version = doc.get('v', '')
                    timestamp = doc.get('timestamp', 0)

                    if artifact_id not in artifacts or timestamp > artifacts[artifact_id]['timestamp']:
                        artifacts[artifact_id] = {
                            'groupId': doc.get('g', ''),
                            'artifactId': artifact_id,
                            'version': version,
                            'timestamp': timestamp
                        }

                # 转换为列表并按 artifactId 排序
                result = sorted(artifacts.values(), key=lambda x: x['artifactId'])
                return result

            except requests.exceptions.SSLError as e:
                self._log(f"🔒 SSL 证书验证失败: {e}")
                if attempt < max_retries - 1:
                    continue
                raise
            except requests.exceptions.Timeout as e:
                self._log(f"⏱️  请求超时: {e}")
                if attempt < max_retries - 1:
                    continue
                raise
            except requests.exceptions.ConnectionError as e:
                self._log(f"🔌 连接错误: {e}")
                if attempt < max_retries - 1:
                    continue
                raise
            except requests.exceptions.RequestException as e:
                self._log(f"⚠️  HTTP 请求错误: {e}")
                if attempt < max_retries - 1:
                    continue
                raise
            except json.JSONDecodeError as e:
                self._log(f"📄 JSON 解析错误: {e}")
                raise
            except Exception as e:
                self._log(f"❓ 未知错误: {e}")
                raise

        return []

    def _search_nexus_group(self, api_url: str, group_id: str, rows: int) -> List[Dict]:
        """从 Nexus 仓库查询（如阿里云镜像）"""
        params = {
            'g': group_id,
            'count': rows
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    wait_time = 2 ** attempt
                    self._log(f"⏳ 等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    self._log(f"🔄 第 {attempt + 1} 次重试...")

                response = self.session.get(api_url, params=params, timeout=30)
                self._log(f"📊 HTTP 状态码: {response.status_code}")
                response.raise_for_status()

                data = response.json()

                # 解析 Nexus 格式的返回结果
                artifacts_data = data.get('data', [])
                self._log(f"📋 原始结果数量: {len(artifacts_data)}")

                artifacts = {}
                for item in artifacts_data:
                    artifact_id = item.get('artifactId', '')
                    # Nexus 返回所有版本，需要找最新的
                    for artifact_hit in item.get('artifactHits', []):
                        for artifact_link in artifact_hit.get('artifactLinks', []):
                            version = artifact_link.get('version', '')
                            if artifact_id not in artifacts or self._compare_versions(version, artifacts[artifact_id]['version']) > 0:
                                artifacts[artifact_id] = {
                                    'groupId': item.get('groupId', ''),
                                    'artifactId': artifact_id,
                                    'version': version,
                                    'timestamp': 0  # Nexus 不提供时间戳
                                }

                result = sorted(artifacts.values(), key=lambda x: x['artifactId'])
                return result

            except Exception as e:
                self._log(f"⚠️  查询失败: {e}")
                if attempt < max_retries - 1:
                    continue
                raise

        return []

    def _compare_versions(self, v1: str, v2: str) -> int:
        """
        比较两个版本号
        返回: 1 如果 v1 > v2, -1 如果 v1 < v2, 0 如果相等
        """
        def version_tuple(v):
            return tuple(map(int, v.split('.')))

        try:
            t1 = version_tuple(v1)
            t2 = version_tuple(v2)
            return (t1 > t2) - (t1 < t2)
        except:
            # 如果版本号格式不标准，按字符串比较
            return (v1 > v2) - (v1 < v2)

    def search_artifact(self, artifact_id: str, group_id: str = "cn.tannn.jdevelops") -> Optional[Dict]:
        """
        搜索指定组件的版本信息

        Args:
            artifact_id: Maven artifactId
            group_id: Maven groupId，默认为 cn.tannn.jdevelops

        Returns:
            组件信息，包含最新版本号
        """
        params = {
            'q': f'g:{group_id} AND a:{artifact_id}',
            'rows': 1,
            'wt': 'json',
            'core': 'gav'
        }

        # 重试机制：最多重试3次
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"🔄 第 {attempt + 1} 次重试...", file=sys.stderr)

                response = self.session.get(self.MAVEN_SEARCH_API, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                docs = data.get('response', {}).get('docs', [])
                if docs:
                    doc = docs[0]
                    return {
                        'groupId': doc.get('g', ''),
                        'artifactId': doc.get('a', ''),
                        'version': doc.get('v', ''),
                        'timestamp': doc.get('timestamp', 0)
                    }
                return None

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"⏱️  请求超时，正在重试 ({attempt + 1}/{max_retries})...", file=sys.stderr)
                    import time
                    time.sleep(2)
                    continue
                else:
                    print(f"❌ 网络请求超时: 已重试 {max_retries} 次仍然失败", file=sys.stderr)
                    print("💡 提示: 请检查网络连接或稍后重试", file=sys.stderr)
                    return None
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  网络错误，正在重试 ({attempt + 1}/{max_retries})...", file=sys.stderr)
                    import time
                    time.sleep(2)
                    continue
                else:
                    print(f"❌ 网络请求失败: {e}", file=sys.stderr)
                    return None
            except Exception as e:
                print(f"❌ 解析数据失败: {e}", file=sys.stderr)
                return None

        return None


def print_maven_dependency(artifact: Dict):
    """打印 Maven 依赖配置"""
    print(f"""
<dependency>
    <groupId>{artifact['groupId']}</groupId>
    <artifactId>{artifact['artifactId']}</artifactId>
    <version>{artifact['version']}</version>
</dependency>
""")


def print_gradle_dependency(artifact: Dict):
    """打印 Gradle 依赖配置"""
    print(f"implementation '{artifact['groupId']}:{artifact['artifactId']}:{artifact['version']}'")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description='查询 JDevelops 组件的最新版本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查询所有 jdevelops 组件
  python query_versions.py

  # 查询指定组件
  python query_versions.py -a jdevelops-apis-result

  # 输出 Maven 依赖格式
  python query_versions.py -a jdevelops-apis-result -f maven

  # 输出 Gradle 依赖格式
  python query_versions.py -a jdevelops-apis-result -f gradle
        """
    )

    parser.add_argument(
        '-a', '--artifact',
        help='指定要查询的 artifactId'
    )

    parser.add_argument(
        '-g', '--group',
        default='cn.tannn.jdevelops',
        help='指定 groupId (默认: cn.tannn.jdevelops)'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['table', 'maven', 'gradle', 'json'],
        default='table',
        help='输出格式: table(表格), maven(Maven依赖), gradle(Gradle依赖), json(JSON格式)'
    )

    args = parser.parse_args()

    checker = JDevelopsVersionChecker()

    if args.artifact:
        # 查询单个组件
        print(f"🔍 正在查询组件: {args.group}:{args.artifact}")
        artifact = checker.search_artifact(args.artifact, args.group)

        if artifact:
            if args.format == 'maven':
                print_maven_dependency(artifact)
            elif args.format == 'gradle':
                print_gradle_dependency(artifact)
            elif args.format == 'json':
                print(json.dumps(artifact, indent=2, ensure_ascii=False))
            else:  # table
                print(f"\n✅ 最新版本: {artifact['version']}")
                print(f"📦 完整坐标: {artifact['groupId']}:{artifact['artifactId']}:{artifact['version']}")
        else:
            print(f"❌ 未找到组件: {args.artifact}")
            sys.exit(1)
    else:
        # 查询所有组件
        print(f"🔍 正在查询所有 {args.group} 组件...")
        artifacts = checker.search_group(args.group)

        if artifacts:
            if args.format == 'json':
                print(json.dumps(artifacts, indent=2, ensure_ascii=False))
            elif args.format == 'maven':
                for artifact in artifacts:
                    print_maven_dependency(artifact)
            elif args.format == 'gradle':
                for artifact in artifacts:
                    print_gradle_dependency(artifact)
            else:  # table
                print(f"\n✅ 找到 {len(artifacts)} 个组件:\n")
                print(f"{'序号':<6} {'ArtifactId':<50} {'最新版本':<15}")
                print("-" * 75)
                for idx, artifact in enumerate(artifacts, 1):
                    print(f"{idx:<6} {artifact['artifactId']:<50} {artifact['version']:<15}")

                print("\n💡 提示:")
                print("  - 查看特定组件详情: python query_versions.py -a <artifactId>")
                print("  - 生成 Maven 依赖: python query_versions.py -a <artifactId> -f maven")
                print("  - 生成 Gradle 依赖: python query_versions.py -a <artifactId> -f gradle")
        else:
            print(f"❌ 未找到任何组件")
            sys.exit(1)


if __name__ == '__main__':
    main()
