@echo off
rem Compile EACS Dataset LaTeX paper to PDF
rem Requires MiKTeX or TeX Live installed

cd /d "C:\Users\Ahmad\OneDrive\Desktop\OPENCODE\EACS Dataset paper preprint"

rem Try pdflatex first
echo Compiling eacs_dataset.tex to PDF...
pdflatex -interaction=nonstopmode eacs_dataset.tex
if %errorlevel% neq 0 (
    echo pdflatex failed, trying xelatex...
    xelatex -interaction=nonstopmode eacs_dataset.tex
)
if %errorlevel% neq 0 (
    echo Compilation failed. Please ensure MiKTeX or TeX Live is installed.
    echo You can download MiKTeX from: https://miktex.org/download
    pause
    exit /b 1
)

echo.
echo "=== PDF compilation complete ==="
echo "Output: eacs_dataset.pdf"
echo.
echo "Opening PDF..."
start "" eacs_dataset.pdf