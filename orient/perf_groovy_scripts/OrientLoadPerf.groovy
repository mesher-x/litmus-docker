t = System.currentTimeMillis()
x = new OrientGraph("memory:"+args[0]+t)
s = System.currentTimeMillis()
x.loadGraphML(args[1])
println System.currentTimeMillis() - s
x.shutdown()
