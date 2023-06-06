echo "AER will be computed using the file:"
echo $1
python aer.py alignmentDeEn.talp $1 --oneRef
