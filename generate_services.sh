for f in `find thrifts/*.thrift`; do
    thrift -r -gen py -out thrifts $f
done