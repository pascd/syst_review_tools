echo "Abstract:" && echo -e $(curl -s http://api.crossref.org/works/10.1155/2016/3845247 2>&1 | \
grep -o -P '(?<=abstract":").*?(?=","DOI)' | \
sed -E 's/<jats:p>|<\\\/jats:p>/\n/g' | \
sed 's/<[^>]*>/ /g')
