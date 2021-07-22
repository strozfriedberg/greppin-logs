FROM ubuntu:focal as ubuntu_base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt upgrade -y && \
    apt autoremove -y

FROM ubuntu_base as greppin_logs

ENV DEBIAN_FRONTEND=noninteractive
# Add installed tools to path
ENV PATH=/opt/tools/bin:$PATH

# Update OS and install:
#   1) Vim (https://www.vim.org/)
#   2) Python3
#   3) Pip for Python3
#   4) venv module for Python3 (https://docs.python.org/3/library/venv.html)
#   5) GNU Parallel (https://www.gnu.org/software/parallel/)
#   6) jq (https://stedolan.github.io/jq/)
RUN apt update && \
    apt upgrade -y && \
    apt autoremove -y && \
    apt install -y vim python3 python3-pip python3-venv parallel jq

# Install custom tools to /opt/tools
WORKDIR /opt/tools

# Install Python tools to virtualenv in /oppt/tools and add to bin
# Includes the following tools/libraries:
#   1) csvkit: https://csvkit.readthedocs.io/en/latest/
#   2) NumPy: https://numpy.org/
#   3) SciPy: https://www.scipy.org/scipylib/index.html
#   4) scikit-learn: https://scikit-learn.org/stable/index.html
#   5) Matplotlib: https://matplotlib.org/
RUN mkdir python-ds bin && \
    python3 -m venv python-ds/venv && \
    . python-ds/venv/bin/activate && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir csvkit numpy scipy pandas scikit-learn matplotlib && \
    ls python-ds/venv/bin/*csv* | while read TOOLPATH; \
    do \
        TOOLNAME="$(basename ${TOOLPATH})"; \
        echo ". /opt/tools/python-ds/venv/bin/activate; ${TOOLNAME} \$@; deactivate" > "bin/${TOOLNAME}"; \
    done && \
    echo ". /opt/tools/python-ds/venv/bin/activate; bash" > bin/enter-python-venv && \
    chmod 777 bin/*csv* bin/enter-python-venv

# Install latest version of R, Rscript, the Tidyverse packages, and the Rush CLI
# See: https://www.digitalocean.com/community/tutorials/how-to-install-r-on-ubuntu-20-04
#      https://www.tidyverse.org/
#      https://github.com/jeroenjanssens/rush
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 && \
    echo 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/' >> /etc/sources.list && \
    apt update && \
    apt install -y r-base r-base-dev libssl-dev libxml2-dev libcurl4-openssl-dev && \
    Rscript -e 'install.packages(c("devtools", "tidyverse"))' && \
    Rscript -e 'devtools::install_github("jeroenjanssens/rush")'

# Install lightgrep CLI
COPY lightgrep-cli/linux/lightgrep /opt/tools/lightgrep/lightgrep
RUN ln -s /opt/tools/lightgrep/lightgrep /opt/tools/bin/lightgrep

WORKDIR /workspaces
