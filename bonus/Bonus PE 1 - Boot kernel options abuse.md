


> To have time to trigger the boot options, we add a delay to the machine boot

![](../Images/Pasted%20image%2020231227193931.png)

When booting the machine, we'll press ctrl + alt + f1 to modify boot options

![](../Images/Pasted%20image%2020231227192250.png)

> By checking the man, we find the interesting init= option
https://www.kernel.org/doc/Documentation/admin-guide/kernel-parameters.txt

> We just have to add this option:
> `init=/bin/bash`

![](../Images/Pasted%20image%2020231227192611.png)

![](../Images/Pasted%20image%2020231227192634.png)\

![](../Images/Pasted%20image%2020231227193720.png)

