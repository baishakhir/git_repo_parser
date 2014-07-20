echo "========== nohup  python ghProc.py $1 >> cpp.out 2>> cpp.err ============"
nohup  python ghProc.py $1 >> cpp.out 2>> cpp.err
#nohup  python ghProc.py ../../study_subjects/$1 > $1.out 2> $1.err
