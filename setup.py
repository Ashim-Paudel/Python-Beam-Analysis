from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="beamframe", 
    version="0.0.1",  
    description="A python module to solve and analyse determinate 2d Beams.", 
    long_description=long_description, 
    long_description_content_type="text/markdown", 
    url="https://ashimp.com.np/beamframe/", 
    author="Ashim Paudel",  
    author_email="paudelashim111@gmail.com",  
    classifiers=[ 
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="beams, frames, structure, civil engineering, structural engineering, applied mechanics", 
    package_dir={"": "src"}, 
    packages=find_packages(where="src"), 
    python_requires=">=3.4, <4",
    install_requires=["numpy>=1.19",
    "sympy>=1",
    "matplotlib>=3"
    ],  
    project_urls={  
        "Source": "https://github.com/Ashim-Paudel/Python-Beam-Analysis",
        "Bug Reports": "https://github.com/Ashim-Paudel/Python-Beam-Analysis/issues",
        "Funding": "https://ashimp.com.np/beamframe/",
        "Say Thanks!": "http://ashimp.com.np/#contact",
    },
)