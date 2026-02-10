class MemoryManager:
    def fifo(self, pages, frames_count):
        frames = []
        page_faults = 0
        snapshots = [] # To visualize memory state at each step

        for page in pages:
            status = "Hit"
            if page not in frames:
                status = "Miss"
                page_faults += 1
                if len(frames) < frames_count:
                    frames.append(page)
                else:
                    frames.pop(0) # Remove first in
                    frames.append(page)
            
            snapshots.append({
                "Page": page,
                "Frames": list(frames), # Copy list
                "Status": status
            })
            
        return page_faults, snapshots

    def lru(self, pages, frames_count):
        frames = []
        page_faults = 0
        snapshots = []
        
        for page in pages:
            status = "Hit"
            if page not in frames:
                status = "Miss"
                page_faults += 1
                if len(frames) < frames_count:
                    frames.append(page)
                else:
                    frames.pop(0) # Remove Least Recently Used (index 0)
                    frames.append(page)
            else:
                # If hit, move it to the end (most recently used)
                frames.remove(page)
                frames.append(page)
                
            snapshots.append({
                "Page": page,
                "Frames": list(frames),
                "Status": status
            })
            
        return page_faults, snapshots