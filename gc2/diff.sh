diff -U 2 ../gc1/fixed/model.py model.py | tail -n +3 > ../../model1to2.diff 
diff -U 2 ../gc1/fixed/gc1.py gc2.py | tail -n +3 > ../../gc1to2.diff
diff -U 2 model.py fixed/model.py | tail -n +3 > ../../model2fix.diff 
diff -U 2 gc2.py fixed/gc2.py | tail -n +3 > ../../gc2fix.diff
