$script:THIS_PATH = $myinvocation.mycommand.path
$script:BASE_DIR = split-path (resolve-path "$THIS_PATH/..") -Parent

$env:PYTHONPATH = "$script:BASE_DIR\src;$script:BASE_DIR\src\generated"
$env:PYTHONDONTWRITEBYTECODE = "YES"
$env:DREPIN_DEBUG = "YES"
