'<!Caution!>
'
'�f�B���N�g���͖������܂�
'
'</!Caution!>

'�ݒ�
str_mpcPath = "C:\Program Files\MPC-BE x64\mpc-be64.exe"

'���C�u��������I�u�W�F�N�g����
Set ShellObj = CreateObject("WScript.Shell")
Set FSObj = createObject("Scripting.FileSystemObject")
Set fileArrayList = CreateObject("System.Collections.ArrayList")

'ArrayList�쐬���[�v
For Each arg In WScript.Arguments
    If Not(FSObj.FolderExists(arg)) Then '�t�@�C���̏ꍇ
        Call fileArrayList.Add(FSObj.GetAbsolutePathName(arg))
    End If
Next

'�����`�F�b�N
If fileArrayList.Count = 0 Then '�t�@�C���w�肪0���̏ꍇ
    WScript.Quit '�I������
End If

'���O���ŕ��בւ�
Call fileArrayList.Sort

'�������Ĕz����擾
names = fileArrayList.ToArray

'ItemList�̍쐬
cmdStr = """" & str_mpcPath & """ /add"
itrMx = UBound(names)
For itr = 0 To itrMx
    cmdStr = cmdStr & " """ & names(itr) & """"
Next    

'�N���b�v�{�[�h�ɃR�s�[
'ShellObj.Exec("clip").StdIn.Write cmdStr

ShellObj.Run cmdStr
