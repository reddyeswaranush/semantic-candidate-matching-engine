# run this once in python shell or as a quick script
from src.full_dataset import load_candidates
from src.storage_manager import save_candidates

candidates = load_candidates()
save_candidates(candidates)
print(f"Saved {len(candidates)} candidates")