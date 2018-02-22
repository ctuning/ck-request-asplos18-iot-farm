#! /bin/bash

# CK installation script for Keras package from ReQuEST @ ASPLOS'18 submission
#
# Developer(s):
#  * Grigori Fursin, dividiti/cTuning foundation
#

# PACKAGE_DIR
# INSTALL_DIR

export PACKAGE_LIB_DIR=${INSTALL_DIR}/lib

######################################################################################
echo ""
echo "Removing '${PACKAGE_LIB_DIR}' ..."
rm -rf ${PACKAGE_LIB_DIR}

######################################################################################
# Print info about possible issues
echo ""
echo "Note that you sometimes need to upgrade your pip to the latest version"
echo "to avoid well-known issues with user/system space installation:"

SUDO="sudo "
if [[ ${CK_PYTHON_PIP_BIN_FULL} == /home/* ]] ; then
  SUDO=""
fi

# Check if has --system option
${CK_PYTHON_PIP_BIN_FULL} install --help > tmp-pip-help.tmp
if grep -q "\-\-system" tmp-pip-help.tmp ; then
 SYS=" --system"
fi
rm -f tmp-pip-help.tmp

######################################################################################
echo "Downloading and installing ..."
echo ""

${CK_PYTHON_PIP_BIN_FULL} install --upgrade -r ${PACKAGE_DIR}/requirements.txt -t ${PACKAGE_LIB_DIR}  ${SYS}
if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

exit 0
