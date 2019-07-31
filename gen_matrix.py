class build_job:
    def __init__(self,name, platform_id, python_versions ) :
        self.name = name
        self.platform_id = platform_id
        self.python_versions = python_versions

windows = build_job( "Windows",
                     "vs2017-win2016",
                     ['3.5.4','3.6.8','3.7.4'] )
mac     = build_job( "MacOS",
                     "macos-10.13",
                     ['2.7.16','3.4.10','3.5.7','3.6.9','3.7.4'] )
linux   = build_job( "Linux",
                     "ubuntu-latest",
                     ['2.7.16','3.4.10','3.5.7','3.6.9','3.7.4'] )
build_jobs = [windows,mac,linux]

for build_job in build_jobs:
        platform_name = build_job.name
        platform      = build_job.platform_id
        for python_version in build_job.python_versions:
            print("    {}_{}:".format(platform_name,python_version))
            print("      vmImage: '{}'".format(platform))
            print("      build_name: '{}_{}_EDM'".format(platform_name,python_version))
            print("      python.version: '{}'".format(python_version))
        
