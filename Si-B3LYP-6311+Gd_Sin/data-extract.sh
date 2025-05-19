#! /bin/bash
##


# function for data extraction
grasp()
{
        scf=`grep "SCF Done" $ast | tail -1 | awk '{print $5}'`
        zpe=`grep "Zero-point correction" $ast |tail -1  | awk '{print $3}'`
        tcg=`grep "Thermal correction to Gibbs Free Energy" $ast |tail -1|awk '{print $7}'`
        etg=`grep "Sum of electronic and thermal Free Energies" $ast | tail -1|awk '{print $8}' `
#       lf=`grep "Low frequencies" $ast | tail -1 |awk '{print $4}'` # | sed s/-//`
        lf=`grep "Frequencies" $ast | head -1 |awk '{print $3}'`

        # check status of output
        n=`tail -10 $ast|grep Normal`
        if [ "k$n" == "k" ]; then
                n=`tail -10 $ast|grep Error`
                if [ "k$n" != "k" ]; then
                        askt="ERROR"
                else
                        askt="NOT FINISHED"
                fi
        else
                askt=""
        fi

        # print out deserved information
        echo "$ast      $scf    $zpe    $tcg    $etg    $lf     $askt"
}

# call function in all available output
for ast  in `ls *.out`; do
        grasp
done
echo " "
for ast  in `ls *.log`; do
        grasp
done

exit 0

