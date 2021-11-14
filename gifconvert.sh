# Uses gifsicle
# Uses imagemagick
echo "Keep general image size of gif"
convert $1 -coalesce tmp-out.gif
gifsicle --flip-horizontal --resize 32x32 --colors 256 tmp-out.gif > out-$1
rm tmp-out.gif

FILES=$(ls -1v out-*);

for file in $FILES ; do
	CONVERT="${CONVERT} ${file}"
done
convert ${CONVERT} +append $1.png
mv $1.png ./icons/
rm -f out-*

