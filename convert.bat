for /r "Content" %%i in (*.htm) DO (
	python strip_footer.py "%%~fi"
	pandoc -f html -t rst "%%~fi" -o "%%~dpni.rst"
)
