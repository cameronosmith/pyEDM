platforms       = [['Linux','ubuntu-16.04'],['Windows','vs2017-win2016'],
                    ['Mac','macos-10.13']]
python_versions = ['2.7','3.4','3.5','3.6','3.7']

for platform_name, platform in platforms:
    for python_version in python_versions:
        print("    {}_{}:".format(platform_name,python_version))
        print("      vmImage: '{}'".format(platform))
        print("      build_name: '{}_{}_EDM'".format(platform_name,platform))
        
