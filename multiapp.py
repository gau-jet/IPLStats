"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st

def get_position(spages,option):
    for i in range(len(spages)):
        
        if spages[i]['title'] == option:
            break
    return i
    
class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        self.apps = []
        self.index=0

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func,            
        })
        self.index = self.index + 1
        
    def run(self):
        tot_pages = len(self.apps)
        cols = st.sidebar.columns(tot_pages)
        query_params = st.experimental_get_query_params()
        if query_params:
            sel_index = get_position(self.apps,query_params['option'][0])
        else:
            sel_index =0
        app = st.sidebar.radio(
           'Go To',
           self.apps,
           index=sel_index,
           format_func=lambda app: app['title'])
        
        but_values = ['false' for i in range(tot_pages)]
                
        try:
            query_option = app['title']            
        except:
            st.experimental_set_query_params(option=app['title'])
            query_params = st.experimental_get_query_params()
            query_option = query_params['option'][0]
        q_index = get_position(self.apps,query_option)
        but_values[q_index] = True
        if "cmenu" not in st.session_state:
            st.session_state.cmenu=0

        if True in but_values:
            c_index = but_values.index(True)            
            if q_index is c_index:                
                final = c_index
                st.experimental_set_query_params(option=self.apps[final]['title'])
            else:                
                final = q_index
        st.session_state.cmenu=final
        self.apps[st.session_state.cmenu]['function']()
        return self.apps[st.session_state.cmenu]['title']

        