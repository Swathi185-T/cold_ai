import torch
from pathlib import Path
from core_preprocessing import FEATURES
from ml.mad_tcn import MADTCN
_model=None
def forecast(sequence):
 global _model
 if _model is None:
  _model=MADTCN(len(FEATURES)); _model.load_state_dict(torch.load(Path('models/mad_tcn_best.pt'),map_location='cpu',weights_only=True)); _model.eval()
 with torch.no_grad(): return _model(torch.tensor(sequence,dtype=torch.float32).unsqueeze(0)).squeeze().tolist()
