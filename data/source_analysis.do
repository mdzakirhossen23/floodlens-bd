* ******************************************************************** *
* ******************************************************************** *
*                                                                      *		
*                   water level graphs					
*                                                                      *
* ******************************************************************** *
* ******************************************************************** *
** IDS VAR:
** NOTES:
** WRITEN BY:        Odbayar Batmunkh
** Last date modified:  nov 6 2024

** Define parts:
gl part1 1 //bangladesh
gl part2 1 //nepal	

cap mkdir "$latex_figures"

** Part 1
if $part1{
	
	*load data
		use "$bgd_round3_dt/Raw/water_level",clear 
		gen date_num=date
		tsset date

	*graph
		twoway (tsline water_level, tlabel(	///
					23542 "Jun 15" ///
					23561 "AA Jul 4" ///
					23589 "Post Shock Aug 4" ///
					23623 "Traditional Sep 4" ///
					23571 "Round 1 Jul 14" ///
					23603 "Round 2 Aug 15" ///
					23637 "Round 3 Sep 18" ///
					, angle(45) ///
					labcolor("black") )) ///
			(scatteri 16 23561 20 23561,recast(line) lcolor(red) ) ///
			(scatteri 16 23571 20 23571,recast(line) lcolor(blue) lpattern(dash)) ///
			(scatteri 19.05 23561 19.05 23573,recast(line) lcolor(black) lpattern(shortdash)) ///			
			(scatteri 16 23589 20 23589,recast(line) lcolor(red) ) ///
			(scatteri 16 23603 20 23603,recast(line) lcolor(blue) lpattern(dash)) ///
			(scatteri 16 23623 20 23623,recast(line) lcolor(red) ) ///
			(scatteri 16 23637 20 23637,recast(line) lcolor(blue) lpattern(dash)) ///
			,legend(order(1 "Water level" 2 "Transfers" 3 "Surveys" 4 "Trigger level" ) ) ///
			ytitle("Water level in meters") xtitle("") /// 
			note("Bahurabad station measured water level.") ///
			title(Bangladesh) ///
			graphregion(color(white)) bgcolor(white) 
			graph export "$latex_figures/water level bangladesh.png", as(png) replace

}

** Part 2
if $part2{

	*load data
		*import excel "$projectfolder/water level/chisapani water level.xlsx", sheet("chisapani water level") firstrow clear
		import delimited "$bgd_round3_dt/Raw/280 chisapani staff gauge GOGI.csv", varnames(8) rowrange(9) clear

	*only keep reading at noon
		keep if reading_hour=="12:00"

		split reading_date,parse(-)

		replace reading_date2="4" if reading_date2=="Apr"
		replace reading_date2="12" if reading_date2=="Dec"
		replace reading_date2="2" if reading_date2=="Feb"
		replace reading_date2="1" if reading_date2=="Jan"
		replace reading_date2="3" if reading_date2=="Mar"
		replace reading_date2="5" if reading_date2=="May"
		replace reading_date2="11" if reading_date2=="Nov"
		replace reading_date2="10" if reading_date2=="Oct"

		destring reading_date1 reading_date2 reading_date3,replace
		replace reading_date3=reading_date3+2000
		gen date=mdy(reading_date2,reading_date1, reading_date3)
		format date %td
		tsset date

		gen date_num=date

		*drop if date<22908

		rename staff_gauge_heightm water_level

	*graph
		twoway (tsline water_level, tlabel(	///
					22919 "Oct 1" ///
					22930 "AA Oct 11" ///
					22976 "Post Shock Nov 22" ///
					22953 "Round 1 Nov 4" ///
					23020 "Round 2 Jan 10" ///
					23159 "Round 3 May 29" ///
					, angle(45) ///
					labcolor("black") )) ///
			(scatteri 2 22930 12 22930,recast(line) lcolor(red) ) ///
			(scatteri 2 22953 12 22953,recast(line) lcolor(blue) lpattern(dash)) ///
			(scatteri 10.8 22919 10.8 22930,recast(line) lcolor(black) lpattern(shortdash)) ///			
			(scatteri 2 22976 12 22976,recast(line) lcolor(red) ) ///
			(scatteri 2 23020 12 23020,recast(line) lcolor(blue) lpattern(dash)) ///
			(scatteri 2 23159 12 23159,recast(line) lcolor(blue) lpattern(dash)) ///
			,legend(order(1 "Water level" 2 "Transfers" 3 "Surveys" 4 "Trigger level" ) ) ///
			ytitle("Water level in meters") xtitle("") /// 
		note("Chisapani station measured water level. ") ///
		title(Nepal) ///
		ysc(r(2.8 12)) xlabel(3(2)12) ///
		graphregion(color(white)) bgcolor(white) 
		graph export "$latex_figures/water level nepal.png", as(png) replace


}
