PYCRYPTO INSTALLATION

1. If encounter error: error: command 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Professional\\VC\\Tools\\MSVC\\14.31.31103\\bin\\HostX86\\x64\\cl.exe' failed with exit code 2

2. In Admin CMD Run: (adjust path according to your MVS version)
"C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvarsx86_amd64.bat"

3. Then Run: (adjust path according to your MVS version)
set CL=-FI"%VCINSTALLDIR%Tools\MSVC\14.16.27023\include\stdint.h

4. Then pip install pycrypto.