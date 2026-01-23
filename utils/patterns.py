"""Pattern matching utilities for DevPulse."""

import re
from pathlib import Path
from typing import List, Tuple


# Tech stack indicators
STACK_PATTERNS = {
    # Languages
    'Node.js': ['package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'],
    'Python': ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile', 'poetry.lock'],
    'Java': ['pom.xml', 'build.gradle', 'build.gradle.kts', 'gradlew'],
    'Go': ['go.mod', 'go.sum'],
    'Rust': ['Cargo.toml', 'Cargo.lock'],
    'Ruby': ['Gemfile', 'Gemfile.lock', 'Rakefile'],
    'PHP': ['composer.json', 'composer.lock'],
    '.NET': ['.csproj', '.fsproj', '.vbproj', 'packages.config', 'nuget.config'],
    'C/C++': ['CMakeLists.txt', 'Makefile', 'configure.ac'],
    'Scala': ['build.sbt', 'build.sc'],
    'Kotlin': ['build.gradle.kts', 'settings.gradle.kts'],
    'Swift': ['Package.swift', '.swift-version'],
    'Dart': ['pubspec.yaml', 'pubspec.lock'],
    'Elixir': ['mix.exs', 'mix.lock'],
    'Haskell': ['stack.yaml', 'cabal.project'],
    'Clojure': ['project.clj', 'deps.edn'],
    
    # Web Languages (detected by extension)
    'HTML': ['*.html'],
    'CSS': ['*.css'],
    'SCSS/Sass': ['*.scss', '*.sass'],
    'Less': ['*.less'],
    'JavaScript': ['*.js', '*.mjs', '*.cjs'],
    'JSX': ['*.jsx'],
    
    # Frontend Frameworks
    'React': ['package.json'],  # Checked via package.json content
    'Vue.js': ['vue.config.js', 'nuxt.config.js', 'nuxt.config.ts'],
    'Angular': ['angular.json', '.angular-cli.json'],
    'Svelte': ['svelte.config.js', 'vite.config.js'],
    'Next.js': ['next.config.js', 'next.config.mjs', 'next-env.d.ts'],
    'Nuxt.js': ['nuxt.config.js', 'nuxt.config.ts'],
    'Gatsby': ['gatsby-config.js', 'gatsby-node.js'],
    'Ember.js': ['ember-cli-build.js', '.ember-cli'],
    
    # Backend Frameworks
    'Django': ['manage.py', 'settings.py'],
    'Flask': ['app.py', 'wsgi.py'],
    'FastAPI': ['main.py'],  # Common pattern
    'Spring Boot': ['application.properties', 'application.yml'],
    'Express.js': ['package.json'],  # Checked via dependencies
    'NestJS': ['nest-cli.json'],
    'Laravel': ['artisan', 'composer.json'],
    'Rails': ['Gemfile', 'config.ru', 'Rakefile'],
    'ASP.NET': ['.csproj', 'Startup.cs'],
    
    # Databases
    'MongoDB': ['.mongorc.js', 'mongod.conf'],
    'PostgreSQL': ['postgresql.conf', '.pgpass'],
    'MySQL': ['my.cnf', 'my.ini'],
    'SQLite': ['.db', '.sqlite', '.sqlite3'],
    'Redis': ['redis.conf', 'dump.rdb'],
    'Cassandra': ['cassandra.yaml'],
    'Elasticsearch': ['elasticsearch.yml'],
    
    # Containerization & Orchestration
    'Docker': ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml', '.dockerignore'],
    'Kubernetes': ['deployment.yaml', 'service.yaml', 'ingress.yaml', 'kustomization.yaml'],
    'Helm': ['Chart.yaml', 'values.yaml'],
    'Vagrant': ['Vagrantfile'],
    
    # CI/CD
    'GitHub Actions': ['.github/workflows/'],
    'GitLab CI': ['.gitlab-ci.yml'],
    'CircleCI': ['.circleci/config.yml'],
    'Travis CI': ['.travis.yml'],
    'Jenkins': ['Jenkinsfile'],
    'Azure Pipelines': ['azure-pipelines.yml'],
    'Bitbucket Pipelines': ['bitbucket-pipelines.yml'],
    
    # Cloud Platforms
    'AWS': ['.aws/', 'aws.json', 'cloudformation.yaml', 'sam.yaml'],
    'Google Cloud': ['app.yaml', 'cloudbuild.yaml', '.gcloudignore'],
    'Azure': ['azure.yaml', 'azuredeploy.json'],
    'Heroku': ['Procfile', 'app.json'],
    'Vercel': ['vercel.json', '.vercel/'],
    'Netlify': ['netlify.toml', '.netlify/'],
    
    # Testing Frameworks
    'Jest': ['jest.config.js', 'jest.config.ts'],
    'Pytest': ['pytest.ini', 'conftest.py'],
    'JUnit': ['pom.xml'],  # Java testing
    'Mocha': ['.mocharc.js', '.mocharc.json'],
    'Cypress': ['cypress.json', 'cypress.config.js'],
    'Playwright': ['playwright.config.js', 'playwright.config.ts'],
    
    # Build Tools
    'Webpack': ['webpack.config.js', 'webpack.config.ts'],
    'Vite': ['vite.config.js', 'vite.config.ts'],
    'Rollup': ['rollup.config.js', 'rollup.config.mjs'],
    'Parcel': ['.parcelrc'],
    'Gulp': ['gulpfile.js', 'gulpfile.babel.js'],
    'Grunt': ['Gruntfile.js', 'Gruntfile.coffee'],
    'Maven': ['pom.xml'],
    'Gradle': ['build.gradle', 'build.gradle.kts', 'settings.gradle'],
    'Make': ['Makefile'],
    
    # Mobile
    'React Native': ['app.json', 'metro.config.js'],
    'Flutter': ['pubspec.yaml', 'flutter_sdk'],
    'Ionic': ['ionic.config.json'],
    'Xamarin': ['.sln', 'App.xaml'],
    
    # Package Managers
    'npm': ['package-lock.json'],
    'Yarn': ['yarn.lock'],
    'pnpm': ['pnpm-lock.yaml'],
    'Composer': ['composer.lock'],
    'Bundler': ['Gemfile.lock'],
    'pip': ['requirements.txt'],
    'Poetry': ['poetry.lock'],
    'Cargo': ['Cargo.lock'],
    
    # Linters & Formatters
    'ESLint': ['.eslintrc', '.eslintrc.js', '.eslintrc.json'],
    'Prettier': ['.prettierrc', '.prettierrc.js', 'prettier.config.js'],
    'Black': ['pyproject.toml'],  # Python formatter
    'Pylint': ['.pylintrc', 'pylintrc'],
    'RuboCop': ['.rubocop.yml'],
    
    # Version Control
    'Git': ['.git/', '.gitignore', '.gitattributes'],
    'Mercurial': ['.hg/', '.hgignore'],
    'SVN': ['.svn/'],
    
    # Documentation
    'Sphinx': ['conf.py', 'index.rst'],
    'MkDocs': ['mkdocs.yml'],
    'Docusaurus': ['docusaurus.config.js'],
    'VuePress': ['.vuepress/config.js'],
    
    # Infrastructure as Code
    'Terraform': ['.tf', 'terraform.tfvars'],
    'Ansible': ['ansible.cfg', 'playbook.yml'],
    'Pulumi': ['Pulumi.yaml'],
    'CloudFormation': ['template.yaml', 'cloudformation.json'],
    
    # Monitoring & Logging
    'Prometheus': ['prometheus.yml'],
    'Grafana': ['grafana.ini'],
    'Sentry': ['.sentryclirc'],
    
    # GraphQL
    'GraphQL': ['schema.graphql', 'schema.gql', 'graphql.config.js'],
    'Apollo': ['apollo.config.js'],
    
    # Other Tools
    'Babel': ['.babelrc', 'babel.config.js'],
    'TypeScript': ['tsconfig.json'],
    'EditorConfig': ['.editorconfig'],
    'pre-commit': ['.pre-commit-config.yaml'],
    'Makefile': ['Makefile'],
    'CMake': ['CMakeLists.txt'],
}


# Secret patterns (regex)
SECRET_PATTERNS = [
    (r'API_KEY\s*=\s*["\']?[\w-]{20,}["\']?', 'API Key'),
    (r'SECRET\s*=\s*["\']?[\w-]{20,}["\']?', 'Secret'),
    (r'TOKEN\s*=\s*["\']?[\w-]{20,}["\']?', 'Token'),
    (r'PASSWORD\s*=\s*["\']?[\w-]{8,}["\']?', 'Password'),
    (r'PRIVATE_KEY\s*=\s*["\']?[\w-]{20,}["\']?', 'Private Key'),
    (r'aws_access_key_id\s*=\s*["\']?[\w-]{20,}["\']?', 'AWS Access Key'),
    (r'aws_secret_access_key\s*=\s*["\']?[\w-]{40,}["\']?', 'AWS Secret Key'),
]


# Common hygiene files
HYGIENE_FILES = {
    'README.md': 'README',
    'README.rst': 'README',
    'README.txt': 'README',
    'README': 'README',
    'LICENSE': 'LICENSE',
    'LICENSE.md': 'LICENSE',
    'LICENSE.txt': 'LICENSE',
    '.gitignore': '.gitignore',
}


def detect_tech_stack(files: List[Path]) -> List[str]:
    """
    Detect technology stack from project files.
    
    Args:
        files: List of file paths in the project
        
    Returns:
        List of detected technologies
    """
    detected = []
    file_names = {f.name for f in files}
    file_extensions = {f.suffix for f in files if f.suffix}
    dir_paths = {str(f.parent.relative_to(f.parents[len(f.parents) - 1])) for f in files}
    
    for tech, indicators in STACK_PATTERNS.items():
        for indicator in indicators:
            # Check for wildcard extension match (e.g., *.html)
            if indicator.startswith('*.'):
                ext = indicator[1:]  # Remove the *
                if ext in file_extensions:
                    detected.append(tech)
                    break
            # Check for exact file match
            elif indicator in file_names:
                detected.append(tech)
                break
            # Check for directory match
            elif indicator.endswith('/') and any(indicator.rstrip('/') in d for d in dir_paths):
                detected.append(tech)
                break
    
    return detected


def scan_for_secrets(file_path: Path) -> List[Tuple[str, int, str]]:
    """
    Scan file for potential secrets.
    
    Args:
        file_path: Path to file to scan
        
    Returns:
        List of tuples (secret_type, line_number, matched_text)
    """
    findings = []
    
    # Only scan text files
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern, secret_type in SECRET_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Truncate matched text for display
                        matched = line.strip()[:80]
                        findings.append((secret_type, line_num, matched))
    except (OSError, UnicodeDecodeError):
        # Skip binary or unreadable files
        pass
    
    return findings


def count_todos(file_path: Path) -> int:
    """
    Count TODO/FIXME comments in file.
    
    Args:
        file_path: Path to file to scan
        
    Returns:
        Number of TODO/FIXME comments found
    """
    count = 0
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            count += len(re.findall(r'\bTODO\b', content, re.IGNORECASE))
            count += len(re.findall(r'\bFIXME\b', content, re.IGNORECASE))
    except (OSError, UnicodeDecodeError):
        # Silently skip files that can't be read - return 0 count
        pass
    
    return count


def check_hygiene_files(root_path: Path) -> dict:
    """
    Check for presence of common hygiene files.
    
    Args:
        root_path: Root directory of project
        
    Returns:
        Dictionary of file type to boolean (exists or not)
    """
    results = {
        'README': False,
        'LICENSE': False,
        '.gitignore': False,
    }
    
    for file_name, file_type in HYGIENE_FILES.items():
        if (root_path / file_name).exists():
            results[file_type] = True
    
    return results
