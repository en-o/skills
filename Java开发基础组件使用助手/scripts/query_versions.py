#!/usr/bin/env python3
"""
JDevelops 组件版本查询工具

用于查询 Maven Central 上 cn.tannn.jdevelops 组件的最新版本信息
"""

import requests
import json
import sys
from typing import List, Dict, Optional


class JDevelopsVersionChecker:
    """JDevelops 版本查询器"""

    # Maven Central Search API
    MAVEN_SEARCH_API = "https://search.maven.org/solrsearch/select"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JDevelops-Version-Checker/1.0'
        })

    def search_group(self, group_id: str = "cn.tannn.jdevelops", rows: int = 100) -> List[Dict]:
        """
        搜索指定 groupId 下的所有组件

        Args:
            group_id: Maven groupId，默认为 cn.tannn.jdevelops
            rows: 返回结果数量，默认 100

        Returns:
            组件列表，每个组件包含 artifactId 和最新版本信息
        """
        params = {
            'q': f'g:{group_id}',
            'rows': rows,
            'wt': 'json',
            'core': 'gav'
        }

        try:
            response = self.session.get(self.MAVEN_SEARCH_API, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # 解析返回结果
            docs = data.get('response', {}).get('docs', [])

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

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {e}", file=sys.stderr)
            return []
        except Exception as e:
            print(f"❌ 解析数据失败: {e}", file=sys.stderr)
            return []

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

        try:
            response = self.session.get(self.MAVEN_SEARCH_API, params=params, timeout=10)
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

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败: {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"❌ 解析数据失败: {e}", file=sys.stderr)
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
  python query_versions.py -a jdevelops-apis-auth

  # 输出 Maven 依赖格式
  python query_versions.py -a jdevelops-apis-auth -f maven

  # 输出 Gradle 依赖格式
  python query_versions.py -a jdevelops-apis-auth -f gradle
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
