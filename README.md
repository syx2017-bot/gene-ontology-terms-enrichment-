# go
#find all go:

(1)初始条件：一个蛋白质列表，但go注释不玩整

(2)目标：找到所有的蛋白质的所有go注释

(3)已有条件：蛋白质/基因列表(格式如genelist.txt)，go数据库文件(下载地址：http://current.geneontology.org/ontology/go-basic.obo）

(4)输出：蛋白质列表下每一个蛋白质ID在go数据库中对应的所有go注释

#go enrichment analysis:

(1)初始条件：基因表达数据,go注释不完整

(2)目标：找到差异表达的基因中哪些go发生了富集

(3)已有条件：基因表达数据(格式如gene_expression.csv)，go数据库文件(下载地址：http://current.geneontology.org/ontology/go-basic.obo）

(4)输出：有显著性差异的go及其p值
