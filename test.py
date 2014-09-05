import pyservi
from commands.utils.semantic import *

sv1 = SemanticVersion('1.0.0')
print(sv1)

sv2 = SemanticVersion('1.2.12')
print(sv2)

assert sv2 > sv1

print('BUMP')
print(sv2)
sv2.bump_ver(MAJOR)
print(sv2)

sv2.bump_ver(MINOR)
print(sv2)

sv2.bump_ver(PATCH)
print(sv2)

sv1 = SemanticVersion('1')
print(sv1)
sv1 = SemanticVersion('1.2')
print(sv1)