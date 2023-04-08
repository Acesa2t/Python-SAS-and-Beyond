/* Analyzing the mtcars dataset and testing out some other functionality. For demonstration purposes.*/

/* Commenting this out so that the focus can stay on the changes 
in the dataset */
/*proc print data=sashelp.cars;
run;*/

/* Used PROC SQL last time, so subsetting and merging with the DATA step this time*/

data cars_subset;
	set sashelp.cars;
	keep Make Model Type Origin EngineSize;
	where Type = 'Sedan';
run;

data cars_subset2;
	set sashelp.cars;
	keep Type MSRP Invoice Horsepower Weight Length;
	where Type = 'Sedan';
run;

/*Merge and add column with price difference later*/
data cars_merged;
	merge cars_subset cars_subset2;
	by Type;
	price_diff = dif(MSRP-INVOICE);
	weight2 = sqrt(weight);
run;

/* Summary stats using PROC SQL and adding new column using CASE WHEN*/

proc sql;
	select MAX(price_diff) as max_price_diff, 
	MIN(price_diff) as min_price_diff, 
	MEAN(price_diff) as mean_price_diff
	from cars_merged;
quit;


proc sql;
	create table cars_new_col as
	select *, 
	case when price_diff > 2.21 then 'High'
	else 'Low' end as price_strata
	from cars_merged;
quit;

/* Graphing 3 of the variables in 3D just to test out G3D*/

proc g3d data=cars_new_col;
	scatter Length*Weight=Horsepower;
run;
quit;

/* Now to do a more formal correlation matrix*/

%let vars=Horsepower EngineSize Weight Length Weight2;
proc corr data=cars_new_col plots(MAXPOINTS=10000)=matrix(histogram);
	var &vars;
run;

proc corr data=cars_new_col;
run;

/* We see that there's a huge risk of collinearity will be running some simple models anyway */

/* Run regression (two SAS methods) although not all linear regression assumptions will be satisfied*/

ods graphics on;
proc reg data=cars_new_col;
   model Horsepower = EngineSize;
quit;

proc glm data=cars_new_col plots(unpack)=diagnostics;
	class Make;
	model Horsepower = Make EngineSize/solution CLPARM;
run;


/*Logistic regression with price_strata. Continous data normally shouldn't be stratified
but again, this is only for demonstration purposes */
proc logistic data=cars_new_col;
	model price_strata = Horsepower;
run;