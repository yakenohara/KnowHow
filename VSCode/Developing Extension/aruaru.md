## あるある

## PJ のクローン後の `npm install` で WARN  

以下のような内容ならきにしなくていい。動作に影響があるわけではない。

```
>npm install
npm WARN test-extension@0.0.1 No repository field.
npm WARN test-extension@0.0.1 No license field.
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@2.1.3 (node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@2.1.3: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})

added 235 packages from 175 contributors and audited 238 packages in 19.375s

31 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities

```

## `vsce package` or `vsce publish` で  `The image ~~ will be broken in README.md.`

以下エラー。  
package.json 内で `repository` の項目が存在しないことが原因。定義する。  

```
 ERROR  Couldn't detect the repository where this extension is published. The image 'assets/images/all-line.gif' will be broken in README.md. Please provide the repository URL in package.json or use the --baseContentUrl and --baseImagesUrl options.
```

## `vsce package` or `vsce publish` で `A 'repository' field is missing from the 'package.json' manifest file.`

以下警告。  
package.json 内で `repository` の項目が存在しないことが原因。定義する。  

```
 WARNING  A 'repository' field is missing from the 'package.json' manifest file.
Do you want to continue? [y/N] y
```

## `vsce publish` で `~~~ already exists. Version number cannot be the same.`

以下エラー。  
package.json 内の `version` の値が、最後に publish した時の内容と同じであることが原因。  
数字をあげる。  

```
>vsce publish
Executing prepublish script 'npm run vscode:prepublish'...

> test@0.0.1 vscode:prepublish D:\test\test
> npm run compile


> test@0.0.1 compile D:\test\test
> tsc -p ./

Publishing xxxtest.test@0.0.1...
 ERROR  xxxtest.test@0.0.1 already exists. Version number cannot be the same.
```
