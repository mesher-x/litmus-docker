import argparse
import os
import glob
import sys
import time
import logging

logging.basicConfig(filename = "Litmus_Benchmark_log.log", level = logging.INFO)
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

graph_based = ['g_sparksee', 'g_orient', 'g_neo4j', 'g_tinker' ]

rdf_based = ['r_rdf3x', 'r_monet', 'r_jena', 'r_arq', 'r_virtuoso' ]

directory_maps = { \
    'g_sparksee':'sparksee', \
    'g_orient' : 'orient', \
    'g_neo4j' : 'neo4j', \
    'g_tinker' : 'tinker', \
    'r_rdf3x' : 'rdf3x', \
    'r_monet' : 'monet', \
    'r_jena' : 'jena', \
    'r_arq' : 'arq', \
    'r_virtuoso' : 'virtuoso'
    }


def gather_data_graph_dms(dms):
    #Gather the data and put it in a csv format
    logger.info("Inside the gather_data_graph_dms for %s" % (dms))
    csv_load = []

    logger.info("Opening the load_logs.log file for %s" % (dms))
    file_handler = open("/var/log/%s/load_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()
    file_handler.close()
    run_id = 1
    logger.info("Succesfuly opened and read the load_logs.log file for %s" % (dms))

    for each in all_lines:
        try:
            csv_load.append([directory_maps[dms], str(run_id), "load", str(int(each.strip()))])
            run_id+=1
        except Exception as e:
            print(e)

    logger.info("Succesfuly processed the load_logs.log file for %s" % (dms))

    for each in csv_load:
        print(",".join(each))

    logger.info("Opening the query_cold_logs.log file for %s" % (dms))
    file_handler = open("/var/log/%s/query_cold_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()[5:]
    file_handler.close()
    logger.info("Succesfuly opened and read the query_cold_logs.log file for %s" % (dms))

    run_id = 0
    csv_query = []
    flag = True
    for each in all_lines:
        if each[0]=="#":
            run_id+=1
            flag = True
            continue;
        if flag:
            query_no = int(each.split("Query ")[1].split("=")[0])
            flag = False
        else:
            try:
                csv_query.append([directory_maps[dms], str(run_id), "query_cold",\
                 str(query_no), str(int(each.strip()))])
                flag = True
            except Exception as e:
                print(e)
    logger.info("Succesfuly processed the query_cold_logs.log file for %s" % (dms))



    
    logger.info("Opening the query_hot_logs.log file for %s" % (dms))
    file_handler = open("/var/log/%s/query_hot_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()[5:]
    file_handler.close()
    logger.info("Succesfuly opened and read the query_hot_logs.log file for %s" % (dms))
    run_id = 0
    flag = True
    for each in all_lines:
        if each[0]=="#":
            run_id+=1
            flag = True
            continue;
        if flag:
            query_no = int(each.split("Query ")[1].split("=")[0])
            flag = False
        else:
            try:
                csv_query.append([directory_maps[dms], str(run_id), "query_hot",\
                 str(query_no), str(int(each.strip()))])
                flag = True
            except Exception as e:
                print(e)
    logger.info("Succesfuly processed the query_hot_logs.log file for %s" % (dms))


    
    for each in csv_query:
        print(",".join(each))

def gather_data_rdf_dms(dms):
    #Gather the data and put it in a csv format
    logger.info("Inside the gather_data_rdf_dms for %s" % (dms))

    csv_load = []

    logger.info("Opening the load_logs.log file for %s" % (dms))

    file_handler = open("/var/log/%s/load_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()
    file_handler.close()
    logger.info("Succesfuly opened and read the load_logs.log file for %s" % (dms))

    run_id = 1
    for each in all_lines:
        csv_load.append([directory_maps[dms], str(run_id), "load", \
            each.strip().split("\t")[2]])
        run_id+=1

    logger.info("Succesfuly processed the load_logs.log file for %s" % (dms))

    logger.info("Opening the query_logs.log file for %s" % (dms))
    file_handler = open("/var/log/%s/query_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()
    file_handler.close()
    logger.info("Succesfuly opened and read the query_logs.log file for %s" % (dms))

    run_id = 0
    query_name = ""
    csv_query = []
    name_flag = True
    for each in all_lines:
        if each[0]=="*":
            run_id = 0
            name_flag = True
            continue;
        if name_flag:
            query_name = each.strip()
            name_flag = False
        else:
            run_id+=1
            csv_query.append([directory_maps[dms], str(run_id), "query", query_name, \
                    each.strip().split("\t")[2]])

    logger.info("Succesfuly processed the query_logs.log file for %s" % (dms))
    
    for each in csv_load:
        print(",".join(each))
    for each in csv_query:
        print(",".join(each))


def g_sparksee(runs, xmlFile):

    logger.info("*"*80)
    logger.info("Running the scripts for the Sparksee DMS")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))
    logger.info("Running the command : /scripts/sparksee/SparkseeLoad.sh %s \
    /tmp/sparksee.gdb %s \
    /var/log/sparksee/load_logs.log" % (runs, xmlFile))
    
    
    #Loading the database
    os.system("/scripts/sparksee/SparkseeLoad.sh %s \
    /tmp/sparksee.gdb %s \
    /var/log/sparksee/load_logs.log" % (runs, xmlFile))

    logger.info("Running the command : /scripts/sparksee/SparkseeQuery.sh %s \
    /tmp/HelloWorld.gdb %s \
    /var/log/sparksee/query_cold_logs.log /scripts/sparksee/SparkseeQueryCold.groovy" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/sparksee/SparkseeQuery.sh %s \
    /tmp/HelloWorld.gdb %s \
    /var/log/sparksee/query_cold_logs.log /scripts/sparksee/SparkseeQueryCold.groovy" % (runs, xmlFile))

    logger.info("Running the command : /scripts/sparksee/SparkseeQuery.sh %s \
    /tmp/HelloWorld.gdb %s \
    /var/log/sparksee/query_hot_logs.log /scripts/sparksee/SparkseeQueryHot.groovy" % (runs, xmlFile))

    os.system("/scripts/sparksee/SparkseeQuery.sh %s \
    /tmp/HelloWorld.gdb %s \
    /var/log/sparksee/query_hot_logs.log /scripts/sparksee/SparkseeQueryHot.groovy" % (runs, xmlFile))

    logger.info("Gathering the info and putting it in a csv file")
    #Gather the data and put it in a csv format
    gather_data_graph_dms("g_sparksee")
    logger.info("*"*80)

def g_tinker(runs, xmlFile):

    logger.info("*"*80)
    logger.info("Running the scripts for the TinkerGraph DMS")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))
    logger.info("Running the command : /scripts/tinker/TinkerLoad.sh %s \
    /tmp/tinker.gdb %s \
    /var/log/tinker/load_logs.log" % (runs, xmlFile))
    
    
    #Loading the database
    os.system("/scripts/tinker/TinkerLoad.sh %s \
    /tmp/tinker.gdb %s \
    /var/log/tinker/load_logs.log" % (runs, xmlFile))

    logger.info("Running the command : /scripts/tinker/TinkerQuery.sh %s \
    /tmp/HelloWorld.gdb.tinker.cold %s \
    /var/log/tinker/query_cold_logs.log /scripts/tinker/TinkerQueryCold.groovy" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/tinker/TinkerQuery.sh %s \
    /tmp/HelloWorld.gdb.tinker.cold %s \
    /var/log/tinker/query_cold_logs.log /scripts/tinker/TinkerQueryCold.groovy" % (runs, xmlFile))

    logger.info("Running the command : /scripts/tinker/TinkerQuery.sh %s \
    /tmp/HelloWorld.gdb.tinker.hot %s \
    /var/log/tinker/query_hot_logs.log /scripts/tinker/TinkerQueryHot.groovy" % (runs, xmlFile))

    os.system("/scripts/tinker/TinkerQuery.sh %s \
    /tmp/HelloWorld.gdb.tinker.hot %s \
    /var/log/tinker/query_hot_logs.log /scripts/tinker/TinkerQueryHot.groovy" % (runs, xmlFile))

    logger.info("Gathering the info and putting it in a csv file")
    #Gather the data and put it in a csv format
    gather_data_graph_dms("g_tinker")
    logger.info("*"*80)


def r_rdf3x(runs, queryLocations, dataFile):
    logger.info("*"*80)
    logger.info("Running the scripts for the RDF3x DMS")
    logger.info("Runs = %s, queryLocations = %s, dataFile = %s" % (runs, queryLocations, dataFile))

    logger.info("Running the command : /scripts/rdf3x/RDF3xLoad.sh %s /tmp rdf3x_graph \
    %s /var/log/rdf3x/load_logs.log" % (runs, dataFile))

    #Loading the database
    os.system("/scripts/rdf3x/RDF3xLoad.sh %s /tmp rdf3x_graph \
    %s /var/log/rdf3x/load_logs.log" % (runs, dataFile)) 
    
    logger.info("Running the command : /scripts/rdf3x/RDF3xExecute.sh /tmp rdf3x_graph \
    %s %s /var/log/rdf3x/query_logs.log %s" % (dataFile, queryLocations, runs))

    #Querying the database
    os.system("/scripts/rdf3x/RDF3xExecute.sh /tmp rdf3x_graph \
    %s %s /var/log/rdf3x/query_logs.log %s" % (dataFile, queryLocations, runs)) 
    
    logger.info("Gathering the info and putting it in a csv file")        
    gather_data_rdf_dms("r_rdf3x")
    logger.info("*"*80)

def g_orient(runs, xmlFile):
    logger.info("*"*80)
    logger.info("Running the scripts for the Orient DMS")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))
    logger.info("Running the command : /scripts/orient/OrientLoad.sh %s \
    /tmp/orient_load.gdb %s /scripts/orient/OrientLoad.groovy \
    /var/log/orient/load_logs.log" % (runs, xmlFile))

    #Loading the database
    os.system("/scripts/orient/OrientLoad.sh %s \
    /tmp/orient_load.gdb %s /scripts/orient/OrientLoad.groovy \
    /var/log/orient/load_logs.log" % (runs, xmlFile))

    logger.info("Running the command : /scripts/orient/OrientQuery.sh %s \
    /tmp/orient_query.gdb %s /scripts/orient/OrientQueryCold.groovy \
    /var/log/orient/query_cold_logs.log" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/orient/OrientQuery.sh %s \
    /tmp/orient_query.gdb %s /scripts/orient/OrientQueryCold.groovy \
    /var/log/orient/query_cold_logs.log" % (runs, xmlFile))

    logger.info("Running the command : /scripts/orient/OrientQuery.sh %s \
    /tmp/orient_query.gdb %s /scripts/orient/OrientQueryHot.groovy \
    /var/log/orient/query_hot_logs.log" % (runs, xmlFile))

    os.system("/scripts/orient/OrientQuery.sh %s \
    /tmp/orient_query.gdb %s /scripts/orient/OrientQueryHot.groovy \
    /var/log/orient/query_hot_logs.log" % (runs, xmlFile))



    logger.info("Gathering the info and putting it in a csv file")
    gather_data_graph_dms("g_orient")
    logger.info("*"*80)


def g_neo4j(runs, xmlFile):
    logger.info("*"*80)
    logger.info("Running the scripts for the Neo4j DMS")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))
    logger.info("Running the command : /scripts/neo4j/Neo4jLoad.sh %s \
    /tmp/neo4j_load.gdb %s \
    /var/log/neo4j/load_logs.log" % (runs, xmlFile))

    #Loading the database
    os.system("/scripts/neo4j/Neo4jLoad.sh %s \
    /tmp/neo4j_load.gdb %s \
    /var/log/neo4j/load_logs.log" % (runs, xmlFile))

    logger.info("Running the command : /scripts/neo4j/Neo4jQuery.sh %s \
    /tmp/neo4j_Query.gdb %s \
    /var/log/neo4j/query_cold_logs.log /scripts/neo4j/Neo4jQueryCold.groovy" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/neo4j/Neo4jQuery.sh %s \
    /tmp/neo4j_Query.gdb %s \
    /var/log/neo4j/query_cold_logs.log /scripts/neo4j/Neo4jQueryCold.groovy" % (runs, xmlFile))
    
    logger.info("Running the command : /scripts/neo4j/Neo4jQuery.sh %s \
    /tmp/neo4j_Query.gdb %s \
    /var/log/neo4j/query_hot_logs.log /scripts/neo4j/Neo4jQueryHot.groovy" % (runs, xmlFile))

    os.system("/scripts/neo4j/Neo4jQuery.sh %s \
    /tmp/neo4j_Query.gdb %s \
    /var/log/neo4j/query_hot_logs.log /scripts/neo4j/Neo4jQueryHot.groovy" % (runs, xmlFile))


    logger.info("Gathering the info and putting it in a csv file")
    gather_data_graph_dms("g_neo4j")
    logger.info("*"*80)


def r_monet():

    pass

def r_jena(runs, queryLocation, dataFile):
    logger.info("*"*80)
    logger.info("Running the scripts for the Jena DMS")
    logger.info("Runs = %s, queryLocations = %s, dataFile = %s" % (runs, queryLocation, dataFile))

    logger.info("Running the command : /scripts/jena/JenaTDBLoad.sh /tmp/ jena_graph \
    %s /var/log/jena/load_logs.log %s" % (dataFile, runs))
 
    #Load the database
    os.system("/scripts/jena/JenaTDBLoad.sh /tmp/ jena_graph \
    %s /var/log/jena/load_logs.log %s" % (dataFile, runs))
    
    logger.info("Running the command : /scripts/jena/JenaTDBExecute.sh /tmp/ jena_graph \
    %s %s /var/log/jena/query_logs.log %s" % (dataFile, queryLocation, runs))

    #Run the query
    os.system("/scripts/jena/JenaTDBExecute.sh /tmp/ jena_graph \
    %s %s /var/log/jena/query_logs.log %s" % (dataFile, queryLocation, runs))

    logger.info("Gathering the info and putting it in a csv file")        
    gather_data_rdf_dms('r_jena')
    logger.info("*"*80)


def r_arq():
    pass

def r_virtuoso(runs, queryLocation, dataFileLocation):
    logger.info("*"*80)
    logger.info("Running the scripts for the Virtuoso DMS")
    logger.info("Runs = %s, queryLocations = %s, dataFile = %s" \
            % (runs, queryLocation, dataFileLocation))

    logger.info("Running the setup_ini.py script to get the configurations ready")
    logger.info("The command is python3 /scripts/virtuoso/setup_ini.py -l /scripts/virtuoso \
            -df %s -qf %s" % (dataFileLocation, queryLocation))
    # All the files which match *.ttl in the dataFile location, would be loaded
    os.system("python3 /scripts/virtuoso/setup_ini.py -l /scripts/virtuoso -df \
            %s -qf %s" % (dataFileLocation, queryLocation))
    
    logger.info("Starting the virtuoso server")
    # Starting the server
    os.system("cd /scripts/virtuoso && /usr/local/virtuoso-opensource/bin/virtuoso-t -f /scripts/virtuoso/ &")
    time.sleep(30)

    logger.info("Runing the command /scripts/virtuoso/virtuoso_load.sh \
    /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/load_logs.log %s" %(runs))     
    # Running the loads
    os.system("/scripts/virtuoso/virtuoso_load.sh /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/load_logs.log %s" %(runs))    
    
    logger.info("Runing the command /scripts/virtuoso/virtuoso_execute.sh \
    /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/query_logs.log %s %s" % (queryLocation, runs))
    # Running the queries
    os.system("/scripts/virtuoso/virtuoso_execute.sh /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/query_logs.log %s %s" % (queryLocation, runs))    
    
    logger.info("Gathering the info and putting it in a csv file")        
    gather_data_rdf_dms('r_virtuoso')    
    logger.info("*"*80)

def create_log_files(list_to_benchmark):
    logger.info("*"*80)
    logger.info("Creating empty log files for all the DMS")
    for each in list_to_benchmark:
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/load_logs.log'))
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/query_cold_logs.log'))
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/query_hot_logs.log'))
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/index_logs.log'))

    logger.info("Created empty log files for all the DMS")
    logger.info("*"*80)

def foo(list_to_benchmark, runs = 10):
    #create_log_files(list_to_benchmark)    
    print(list_to_benchmark)
    pass

def write_csv_file(csv_list, filename):
    file_handler = open(filename, "w")
    for each in csv_list:
        file_handler.write(",".join(each) + "\n");
    file_handler.close()

def get_name_of_file(file_location):
    try:
        return file_location.split("/")[-1]
    except Exception as e:
        return file_location

def generate_rdf_queries(rdf_query_location):
    """This function will generate SPARQL query file for the 
    Virtuoso RDF Model and the Apache Jena"""
    logger.info("*"*80)
    logger.info("Creating rdf query files from queries present at %s \
        for Jena (/jena_queries) and Virtuoso (/virtuoso_queries)" % (rdf_query_location))
    os.mkdir("/virtuoso_queries")
    os.mkdir("/jena_queries")
    all_sparql = glob.glob(rdf_query_location + "/*.sparql")
    for each in all_sparql:
        new_file = open("/virtuoso_queries/" + get_name_of_file(each), "w")
        original_file = open(each, "r").read()
        new_file.write("SPARQL;\n")
        new_file.write(original_file)
        new_file.close()
        apache_file = open("/jena_queries/" + get_name_of_file(each), "w")
        apache_file.write(original_file.split(";")[0])
        apache_file.close()
    logger.info("Created rdf query files from queries present at %s \
        for Jena (/jena_queries) and Virtuoso (/virtuoso_queries)" % (rdf_query_location))
    logger.info("*"*80)

def generate_graph_queries(gremlin_query_location_cold, gremlin_query_location_hot = None):
    """This function will generate the custom groovy files for all 
        the three graph based dbs"""
    if gremlin_query_location_hot is None:
        gremlin_query_location_hot = gremlin_query_location_cold
    logger.info("*"*80)
    logger.info("Creating gremlin query files from gremlin_cold.groovy file present at %s \
        for Gremlin cold cache for Orient, Neo4j and Sparksee" % (gremlin_query_location_cold))
    
    gremlin_queries = open(gremlin_query_location_cold, "r").read()
    sparksee_filehandler = open("/scripts/sparksee/SparkseeQueryCold.groovy", "w")
    sparksee_filehandler.write("""import com.tinkerpop.blueprints.impls.sparksee.*

x = new SparkseeGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
no_of_times = Integer.parseInt(args[2])
println "==============Running The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    sparksee_filehandler.write(gremlin_queries)
    sparksee_filehandler.write("""}
x.shutdown()""");
    sparksee_filehandler.close()

    tinker_filehandler = open("/scripts/tinker/TinkerQueryCold.groovy", "w")
    tinker_filehandler.write("""x = new TinkerGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
no_of_times = Integer.parseInt(args[2])
println "==============Running The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    tinker_filehandler.write(gremlin_queries)
    tinker_filehandler.write("""}
x.shutdown()""");
    tinker_filehandler.close()


    neo4j_filehandler = open("/scripts/neo4j/Neo4jQueryCold.groovy", "w")
    neo4j_filehandler.write("""x = new Neo4jGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();

no_of_times = Integer.parseInt(args[2])
println "==============Starting to Run The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""");
    neo4j_filehandler.write(gremlin_queries)
    neo4j_filehandler.write("""}
x.shutdown()""")
    neo4j_filehandler.close()    

    orient_filehandler = open("/scripts/orient/OrientQueryCold.groovy", "w")
    orient_filehandler.write("""println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x = new OrientGraph("memory:"+args[0])
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();

no_of_times = Integer.parseInt(args[2])
println "==============Starting to Run The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    orient_filehandler.write(gremlin_queries)
    orient_filehandler.write("""}
x.shutdown()""")
    orient_filehandler.close()


    gremlin_queries = open(gremlin_query_location_hot, "r").read()
    sparksee_filehandler = open("/scripts/sparksee/SparkseeQueryHot.groovy", "w")
    sparksee_filehandler.write("""import com.tinkerpop.blueprints.impls.sparksee.*

x = new SparkseeGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
no_of_times = Integer.parseInt(args[2])
println "==============Running The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    sparksee_filehandler.write(gremlin_queries)
    sparksee_filehandler.write("""}
x.shutdown()""");
    sparksee_filehandler.close()


    tinker_filehandler = open("/scripts/tinker/TinkerQueryHot.groovy", "w")
    tinker_filehandler.write("""
x = new TinkerGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
no_of_times = Integer.parseInt(args[2])
println "==============Running The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    tinker_filehandler.write(gremlin_queries)
    tinker_filehandler.write("""}
x.shutdown()""");
    tinker_filehandler.close()

    neo4j_filehandler = open("/scripts/neo4j/Neo4jQueryHot.groovy", "w")
    neo4j_filehandler.write("""x = new Neo4jGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();

no_of_times = Integer.parseInt(args[2])
println "==============Starting to Run The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""");
    neo4j_filehandler.write(gremlin_queries)
    neo4j_filehandler.write("""}
x.shutdown()""")
    neo4j_filehandler.close()    

    orient_filehandler = open("/scripts/orient/OrientQueryHot.groovy", "w")
    orient_filehandler.write("""println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x = new OrientGraph("memory:"+args[0])
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();

no_of_times = Integer.parseInt(args[2])
println "==============Starting to Run The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    orient_filehandler.write(gremlin_queries)
    orient_filehandler.write("""}
x.shutdown()""")
    orient_filehandler.close()




    logger.info("Creating gremlin query files from gremlin_hot.groovy file present at %s \
        for Hot Cache for Orient, Neo4j and Sparksee" % (gremlin_query_location_hot))



    logger.info("*"*80)

def sanity_checks(args):
    logger.info("*"*80)
    logger.info("Running the sanity checks")
    is_sane = True
    if not os.path.exists(args["graph_datafile"]):
        print("Incorrect Path.")
        logger.error("Incorrect path to the graph_datafile argument")
        return False
    else:
        s = glob.glob(args["graph_datafile"] + "/*")
        if len(s)!=1:
            print("Please make sure there is only one file in the specified \
                graph_datafile directory")
            logger.error("There has to be only one Graphml file in the directory which is \
                given as an argument to the graph_datafile argument")
            return False
    logger.info("graph_datafile argument is valid")

    if not os.path.exists(args["rdf_datafile"]):
        logger.error("Incorrect directory supplied to the rdf_datafile argument")
        print("The directory does not exist")  
    else:
        s = glob.glob(args["graph_datafile"] + "/*")
        if len(s)!=1:
            print("Please make sure there is only one file in the specified \
                rdf_datafile directory")
            logger.error("There has to be only one Graphml file in the directory which is \
                given as an argument to the graph_datafile argument")

            return False
    logger.info("rdf_datafile argument is valid")
  
        
    if not os.path.exists(args["graph_queries"]):
        print("The graph query file does not exist")
        logger.error("The directory supplied as an argument to graph_queries \
                argument does not exist")
        return False
    else:
        s = glob.glob(args["graph_queries"]+"/gremlin.groovy.*")
        if len(s)!=2:
            print("Please make sure that the file gremlin.groovy.hot_cache and \
                    gremlin.groovy.cold_cache is present in the dataset")
            logger.error("The directory supplied as an argument needs to have \
            two files with the name gremlin.groovy.hot_cache and gremlin.groovy.cold_cache")

            return False

    logger.info("graph_queries argument is valid")

    if not os.path.exists(args["rdf_queries"]):
        logger.error("The directory supplied as an argument to rdf_queries \
                argument does not exist")
        print("The Sparql queries do not exist")
    else:
        s = glob.glob(args["rdf_queries"]+ "/*.sparql")
        if len(s) == 0:
            logger.error("Could not find any sparql queries in the path which\
            was given as an argument to rdf_queries")
            print("No sparql files exist")
            return False
    
    logger.info("rdf_queries argument is valid")
    logger.info("All the arguments are valid") 
    return True


if __name__ == "__main__":
    logger.info("Litmus Benchmark Suite")
    parser = argparse.ArgumentParser(description='The Litmus Benchmark Suite')
    parser.add_argument('-gd', '--graph_datafile', help='The location of the Graph Database File', required = True)
    parser.add_argument('-rd', '--rdf_datafile', help='The location of the RDF Database File', required = True)
    parser.add_argument('-gq', '--graph_queries', help='The location of the Gremlin Queries', required = True)
    parser.add_argument('-rq', '--rdf_queries', help = 'The location of the Sparql Queries', required = True)    
    parser.add_argument('-v', '--verbose', action = "store_true", help = "Verbose", required = False)
    parser.add_argument('-a','--all', action = "store_true" , help='Run for all DMS', required=False)
    parser.add_argument('-g','--graph', action = "store_true", help='Run for all Graph Based DMS', required=False)
    parser.add_argument('-r','--rdf', action = "store_true", help='Run for all RDF Based DMS', required=False)
    parser.add_argument('-n', '--runs', help='Number of times, the experiment should be conducted', required = False)
    
    
    args = vars(parser.parse_args())
    if not sanity_checks(args):
        sys.exit(-1)
    
    final_list = None
    verbose = args['verbose']
    if args['all'] or (args['graph'] and args['rdf']):
        final_list = graph_based + rdf_based
        args['graph'] = True
        args['rdf'] = True
    elif args['graph']:
        final_list = graph_based 
    elif args['rdf']:
        final_list = rdf_based
    else:
        final_list = graph_based + rdf_based
    total_runs = None 
    try:
        total_runs = int(args['runs'])
    except Exception as e:
        total_runs = 5
    #foo(final_list, runs = total_runs)
    logger.info("Runs = %d,  Graph_Data_Location = %s, \
                Graph_query_Location = %s, \
                RDF_Data_Location = %s, \
                RDF_Query_Location = %s." 
        % (total_runs, args['graph_datafile'], args['graph_queries'], args['rdf_datafile'], args['rdf_queries']))
    
    if args['graph']:
        generate_graph_queries(args['graph_queries']+"/gremlin.groovy.cold_cache", \
                args['graph_queries']+"/gremlin.groovy.hot_cache")
        name_of_graph = glob.glob(args['graph_datafile'] + "/*")
        name_of_graph = name_of_graph[0]
        g_sparksee(total_runs, name_of_graph)
#        g_orient(total_runs, name_of_graph)
#        g_neo4j(total_runs, name_of_graph)
        g_tinker(total_runs, name_of_graph)
    if args["rdf"]:
        generate_rdf_queries(args['rdf_queries'])
        name_of_graph = glob.glob(args['rdf_datafile'] + "/*.ttl")
        name_of_graph = name_of_graph[0]
        create_log_files(final_list)
        r_virtuoso(total_runs, "/virtuoso_queries", args['rdf_datafile'])
        r_rdf3x(total_runs, args['rdf_queries'], name_of_graph)
        r_jena(total_runs, "/jena_queries", name_of_graph)

