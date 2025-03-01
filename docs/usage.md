# Usage

# Run as docker container

Inside the docker container, the API is exposed on port 5000. You can map this to any
port on your host machine, in this example we use port 8000.

```bash
docker run -d -p 8000:5000 marhoy/meteogram
```

## Query the API

After starting the container, you can open a web browser to see a small meteogram for
the peak of Kilimanjaro:
<http://localhost:8000/meteogram?lat=-3.0674&lon=37.3556&altitude=5895>

Alternatively, you could download that image to a file using `curl`:

```bash
curl -o kilimanjaro_small.png "http://localhost:8000/meteogram?lat=-3.0674&lon=37.3556&altitude=5895"
```

# Run as Python package

You can also use the package as a Python library:

```bash
pip install meteogram
```

In order to produce a meteogram for Kilimanjaro and save it to a file, you could do
something like this:

```python
from meteogram import Location, create_meteogram

# Location: The peak of Kilimanjaro
location = Location(lat=-3.0674, lon=37.3556, altitude=5895)
fig = create_meteogram(location, hours=48, size_x=800, size_y=400)

# Save to file
fig.savefig("meteogram.png", dpi=300, bbox_inches="tight")
```
