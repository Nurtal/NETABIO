
"""
"""
import os

__version__ = "0.0.1"
_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_script_path(path):
	return os.path.join(_ROOT, 'scripts', path)

## Get path for R script
CORRELATIONMATRIX_SCRIPT = get_script_path('fs_correlation_matrix_analysis.R')
ATTRIBUTEIMPORTANCE_SCRIPT = get_script_path('fs_attribute_importance_evaluation.R')
RFE_SCRIPT = get_script_path('fs_RFE_analysis.R')
BORUTA_SCRIPT = get_script_path('fs_Boruta_analysis.R')