# `gcc` `g++` `make`

`i686-w64-mingw32-gcc` とか書かずに、単に `gcc` とコマンドを打てば使えるようになるパッケージの組み合わせ。  
`gcc`, `g++`, `make` コマンドと 各実行環境毎に以下の組み合わせ。


| コマンド名 |     Cygwin環境の場合     |                   MSYS2環境 の場合                   |
| :--------: | :----------------------: | :--------------------------------------------------: |
|    gcc     | `Devel` -> `gcc-core` ※1 | `mingw64-i686-gcc-core` or `mingw-w64-x86_64-gcc` ※2 |
|    g++     |   `Devel` -> `gcc-g++`   | `mingw64-i686-gcc-core` or `mingw-w64-x86_64-gcc` ※2 |
|    make    |    `Devel` -> `make`     |                      `make`  ※3                      |


※1  
`Devel` -> `mingw64-i686-gcc-core`, `Devel` -> `mingw64-x86_64-gcc-core` はダメ。  
これらをインストールした場合は、`gcc` コマンドの代わりに `i686-w64-mingw32-gcc`, `x86_64-w64-mingw32-gcc` を使用する必要がある。  

※2  
どちらかをインストールすれば、`g++` が使えるようになる。  
また、単なる `gcc` はダメ。`mingw-` 付きの gcc と違い、なぜか `g++` はインストールされない。  

※3  
make ツールなら、 `mingw-w64-i686-make`, `mingw-w64-x86_64-make` もあるけど、  
これらをインストールした場合は、`make` コマンドの代わりに `mingw32-make` を使用する必要がある。  
`mingw-w64-i686-make 4.2.1-4` or `mingw-w64-x86_64-make 4.2.1-4` で確認。  
バージョンによっては `msys-make` かもしれない。  
