from flask import Flask, render_template, request 
from reader import *
from datasets import *
app= Flask(__name__)



@app.route("/")
def homepage():
    #extract a subset of initial 200 entries
    sample=data.df.iloc[:200, :]

    #create table
    table= sample.to_html()
    return render_template("Homepage.html", table= table)


@app.route("/Active_Operations")
def active_operations():
    names= {"get_columns": "Get Columns", "get_ID": "Get Unique ID", "get_type": "Get Unique Type", "count_entries": "Get Number of Entries for Type", "get_chromosomes": "Get Whole Chromosome Dataset", "count_fragmented": "Get Fraction of Fragmented Features" , "get_ens_hav": "Get Ensembl-Havana Dataset", "count_ens_hav":"Count Entries in Ensembl-Havana Dataset:", "get_gene_names":"Get Genes Names" }
    menu_values= Operation._get_register()
    active_op= { i: names[i] for i in menu_values}
   
    return render_template("Active_Operations.html", active_op= active_op )


@app.route("/Operation")
def operation():
    
    op_dict= {"get_columns": get_columns(), "get_ID": get_ID(),  "get_type": get_type(), "count_entries": count_entries(), "get_chromosomes": get_chromosomes(), "count_fragmented": count_fragmented() , "get_ens_hav": get_ens_hav(), "count_ens_hav": count_ens_hav(), "get_gene_names":get_gene_names() }
    op_type=request.args.get('value') 
    operator= op_dict[op_type]
    result= operator.run(data).show_result()
    
    table_templ= False
    #if the result is a dataframe, instead of returning the result of the operation, returns the html format of the dataframe table, which will be directly read by jinja as html code. 
    if isinstance(result, pd.DataFrame):
        result = result.to_html(max_rows=2000)
        table_templ= True
        
    

    return render_template("Operation.html", result= result, table_templ= table_templ )

@app.route("/Documentation")
def documentation():
    return render_template("Documentation.html")

if __name__== "__main__":
    app.run(debug=True)
