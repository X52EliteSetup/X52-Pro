# coding: utf-8


import invoke
import argparse
import os

from config import source_location, pr_location, elite_location
from config import filename_binds, filename_profile, filename_profile_custom

# trying to do an installer for the files, with auto retrieve for updates
def locations_exist():
    """verify that all locations are dirs and have the files"""
    # TODO: perform this checks on all dirs after initial setup
    # this are all the locations for the files. the source, where all lives, and pr and elite where the saitek tool's and elite's folders are.
    a = os.path.isdir(source_location)
    b = os.path.isdir(pr_location)
    c = os.path.isdir(elite_location)
    return (a and b and c)

    
def cp(a,b):
    """run a copy file from a to b"""
    c = invoke.run('cp "{}" "{}" '.format(a,b), warn=True)
    return c
    

def deploy_files():
    """put the files in the right places"""
    local_profile = os.path.join(source_location, filename_profile_custom)
    local_bindings = os.path.join(source_location, filename_binds)
    c = cp(local_profile, pr_location)
    d = cp(local_bindings, elite_location) 
    if not c.ok or not d.ok:
        print("FAIL: Some shit went wrong on deployment")
    return (c.ok and d.ok)

    
def collect_files():
    """get all the files from the deployed locations"""
    # oops, we should make sure we are in the right location first of all.
    # first get the profile, then the bindings.
    profile_path = os.path.join(pr_location,filename_profile_custom) 
    profile_destiny= os.path.join(source_location, filename_profile)
    bindings_path = os.path.join(elite_location, filename_binds)
    #TODO: Stash the files before collecting???
    c = invoke.run('cp "{}" "{}"'.format(profile_path, profile_destiny), warn=True)
    d = invoke.run('cp "{}" "{}"'.format(bindings_path, source_location), warn=True)
    diff = invoke.run("git diff")
    if not c.ok or not d.ok:
        print("FAIL: Some shit went wrong while copyng files")
    return (c.ok and d.ok)
        
def check_files():
    """verify that all is good with the files and if they have changes"""
    if locations_exist():
        a = invoke.run("git status")
    return a.ok

if __name__=="__main__":
    # and then do all the argparse stuff 
    a = argparse.ArgumentParser(description="manage your ED config files, to make it easier to have your files under version control")
    a.add_argument("operation", nargs="?", help="Choose to 'deploy' or 'collect' the files", choices=("deploy","collect","check"), default="check")
    #a.title="choose to deploy or collect the files modified by E:D or Profile Editor"

    opts = a.parse_args()

    if not locations_exist():
        print("WTF Dude, create the folders you need to work")
        #TODO: Have a nicer way of addressing the creation of files and folders, and asking the user.
        exit(1)

    perform = { 
            "deploy":deploy_files,
            "collect":collect_files,
            "check":check_files,
            }
    perform[opts.operation]()


