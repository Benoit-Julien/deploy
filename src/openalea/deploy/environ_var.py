################################################################################
# -*- python -*-
#
#       OpenAlea.Deploy : OpenAlea setuptools extension
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

__license__ = "Cecill-C"
__revision__ =" $Id$"

__doc__ = """ Environment variable manipulation functions """


import os
import sys


def set_lsb_env(name, vars):
    """
    Write a sh script in /etc/profile.d which set some environment variable
    LIBRARY_PATH and PATH are processed particulary in order to avoid overwriting
    @param name : file name string without extension
    @param vars : ['VAR1=VAL1', 'VAR2=VAL2', 'LIBRARY_PATH=SOMEPATH' ]
    """

    if(not 'posix' in os.name): return

    # Build string
    exportstr = ""
    
    for newvar in vars:

        vname, value = newvar.split('=')
        if(((vname == "LD_LIBRARY_PATH") or (vname== "PATH")) and value):
            exportstr += 'if [ -z "$%s" ]; then\n'%(vname)
            exportstr += '  export %s=%s\n'%(vname, value,)
            exportstr += 'else\n'
            exportstr +='  export %s=$%s:%s\n'%(vname, vname, value,)
            exportstr += 'fi\n\n'
                    
        elif(vname and value):
            exportstr += 'export %s=%s\n\n'%(vname, value)
    

    filename = '/etc/profile.d/'+name+'.sh'
    try:
        filehandle = open(filename, 'w')
    except:
        print "ERROR : Cannot create /etc/profile.d/%s.sh"%(name)
        print "ERROR : Check if you have Root privileges, or if your " + \
              "system support this feature.\n"
        print "\nIMPORTANT !!!"
        print "Add the following lines to your /etc/profile or your ~/.bashrc :\n"
        print exportstr
        raise
    
    print "Creating %s"%(filename,)
    
    filehandle.write("# This file has been generated by OpenAlea.Deploy\n\n")
    filehandle.write(exportstr)
            
    filehandle.close()
    #cmdstr = "(echo $SHELL|grep bash>/dev/null)&&. %s||source %s"%(filename,filename)
    #print "Executing :", cmdstr
    os.system(cmdstr)



def set_win_env(vars):
    """
    Set Windows environment variable persistently by editing the registry
    @param vars : ['VAR1=VAL1', 'VAR2=VAL2', 'PATH=SOMEPATH' ]
    """

    if(not 'win32' in sys.platform):
        return
    
    for newvar in vars:

        from string import find
          
        try:
            import _winreg 

        except ImportError, e:
            print "!!ERROR: Can not access to Windows registry."
            return

        def queryValue(qkey, qname):
            qvalue, type_id = _winreg.QueryValueEx(qkey, qname)
            return qvalue

        regpath = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        key = _winreg.OpenKey(reg, regpath, 0, _winreg.KEY_ALL_ACCESS)
        
        name, value = newvar.split('=')

        # Specific treatment for PATH variable
        if name.upper() == 'PATH':
            value= os.path.normpath(value)
            actualpath = queryValue(key, name)
            
            listpath = actualpath.split(';')                
            if not (value in listpath):
                value = actualpath + ';' + value
                print "ADD %s to PATH" % (value,)
            else :
                value = actualpath
            
        if(name and value):
            
            expand = _winreg.REG_SZ
            # Expand variable if necessary
            if("%" in value):
                expand = _winreg.REG_EXPAND_SZ
                
            _winreg.SetValueEx(key, name, 0, expand, value)
                        
            os.environ[name] = value
            
        _winreg.CloseKey(key)    
        _winreg.CloseKey(reg)

    # Refresh Environment
    try:
        HWND_BROADCAST      = 0xFFFF
        WM_SETTINGCHANGE    = 0x001A
        SMTO_ABORTIFHUNG    = 0x0002
        sParam              = "Environment"

        import win32gui
        res1, res2          = win32gui.SendMessageTimeout(HWND_BROADCAST,
                                WM_SETTINGCHANGE, 0, sParam, SMTO_ABORTIFHUNG, 100)
        if  not res1:
            print ("result %s, %s from SendMessageTimeout" % (bool(res1), res2))
        
    except Exception, e:
        print e


