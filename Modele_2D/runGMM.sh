set -e


python genererGamme.py
#
python leaveOneOutEstimation_v2.py pc N
python leaveOneOutEstimation_v2.py pc U
python leaveOneOutEstimation_v2.py k N
python leaveOneOutEstimation_v2.py k U
#
python leaveOneOutEstimationPerGamme.py pc N
python leaveOneOutEstimationPerGamme.py pc U
python leaveOneOutEstimationPerGamme.py k N
python leaveOneOutEstimationPerGamme.py k U
#
python customRespSurf.py pc N
python customRespSurf.py pc U
python customRespSurf.py k N
python customRespSurf.py k U

python compareSobol.py pc N
python compareSobol.py pc U
python compareSobol.py k N
python compareSobol.py k U

python comparePdf.py pc N
python comparePdf.py pc U
python comparePdf.py k N
python comparePdf.py k U

python PDFAnalysis.py pc N
python PDFAnalysis.py pc U
python PDFAnalysis.py k N
python PDFAnalysis.py k U
