with open('scratch/patch_res/UIFollowonFacebook.nxs', 'rb') as f:
    data = f.read()
print(f"UIFollowonFacebook.nxs length: {len(data)}")
print("magic:", data[:4])
