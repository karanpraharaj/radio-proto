from pydantic import BaseModel

class Findings(BaseModel):
    Kidneys: str = None
    Ureters: str = None
    Urinary_bladder: str = None
    Reproductive_organs: str = None
    Lower_chest: str = None
    Liver: str = None
    Gallbladder: str = None
    Bile_ducts: str = None
    Spleen: str = None
    Pancreas: str = None
    Adrenal_glands: str = None
    Vasculature: str = None
    Lymph_nodes: str = None
    Bowel: str = None
    Peritoneum: str = None
    Abdominal_wall: str = None
    Bones: str = None