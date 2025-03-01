# Usage

# Run as docker container

```bash
docker run -d -p 8000:5000 marhoy/meteogram
```

## Query the API

```bash
curl "http://localhost:8000/meteogram?lat=60.4181439&lon=7.2490061&hours=90"
```

# Run as Python package

```bash
pip install meteogram
```

```python
from meteogram import Location, create_meteogram

location = Location(lat=60.4181439, lon=7.2490061)
fig = create_meteogram(location, hours=90, size_x=1000, size_y=400)

# Save to file
fig.savefig("meteogram.png", dpi=300, bbox_inches="tight")
```
