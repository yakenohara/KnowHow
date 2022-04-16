# Cygwin��OpenSSH�̃C���X�g�[��������

CygwinInstaller�������āAopennssh���C���X�g�[������

![openssh](asset/picture/openssh.png)

# Cyg-run service�̃C���X�g�[��&�N��

�uWindows�v���u�X�^�[�g�v����A�uCygwin64 Terminal�v���Ǘ��Ҍ����Ŏ��s���܂��B

�ussh-host-config�v�ƃ^�C�v����Enter�B���₪����̂ŁA�ȉ��̂悤�ɉ񓚂��܂��B

```
*** Query: Should StrictModes be used? (yes/no) yes
*** Query: Should privilege separation be used? <yes/no>: yes
*** Query: New local account 'sshd'? <yes/no>: yes
*** Query: Do you want to install sshd as a service?
*** Query: <Say "no" if it is already installed as a service> <yes/no>: yes
*** Query: Enter the value of CYGWIN for the deamon: [] binmode ntsec
*** Query: Do you want to use a different name? (yes/no) no
*** Query: Create new privileged user account 'cyg_server'? (yes/no) no
*** Query: Do you want to proceed anyway? (yes/no) yes
```

���̌�A`cygrunsrv -S sshd`�ƃ^�C�v����Enter�B
���̌�A`netsh advfirewall firewall add rule name="sshd" dir=in action=allow protocol=TCP localport=22`�ƃ^�C�v����Enter�B

�ȏ�ŁA��PC����SSH�Ń��O�C���ł��܂��B

# ��Cyg-run Service���폜����ꍇ

�ȉ��̂悤�ɂ��܂�

## ���݂̓��쒆�̃T�[�r�X���m�F

```
#cygrunsrv -L
sshd
```

## �T�[�r�X�̒�~�E�폜

```
#cygrunsrv --stop sshd
#cygrunsrv --remove sshd
```

## ���[�U����폜

```
#net user sshd /delete
```