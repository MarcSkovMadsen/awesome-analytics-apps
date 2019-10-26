"""Here we import the different task submodules/ collections"""
from invoke import Collection, task

from tasks import docker, sphinx, package, test

# pylint: disable=invalid-name
# as invoke only recognizes lower case
namespace = Collection()
namespace.add_collection(test)
namespace.add_collection(docker)
namespace.add_collection(package)
namespace.add_collection(sphinx)
