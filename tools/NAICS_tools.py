import pandas as pd

def clean_up_2022_NAICS_Descriptions(df):
    """
    The input data frame df has columns 'Code', 'Title', and 'Description'
    This function cleans up the input data frame by doing the following
    * in the column 'Code', the value `31-33` is replaced with `31`
    * in the column 'Code', the value `44-45` is replaced with `44`
    * in the column 'Code', the value `48-49` is replaced with `48`
    * the dtype of the column  'Code' is changed to `int`
    * Column 'Title' contains a string. Where that string ends with a 'T' (capital letter 'T'), that letter is removed
    """

    df_clean = df

    # Replace values in the 'Code' column
    df_clean['Code'] = df_clean['Code'].replace({'31-33': '31', '44-45': '44', '48-49': '48'})
    
    # Convert 'Code' column to integer dtype
    df_clean['Code'] = df_clean['Code'].astype(int)

    # Remove 'T' from the end of strings in 'Title' column
    df_clean['Title'] = df_clean['Title'].str.rstrip('T')

    return df_clean



def get_children(key_val, df, key_col='Code'):
    # NAICS 2022 specific
    
    # special treatment for the special top level sectors
    if (key_val==31):
        lower = 310
        upper = 340
    elif (key_val==44):
        lower = 440
        upper = 460
    elif (key_val==48):
        lower = 480
        upper = 500
    elif (key_val==0): 
        lower = 0
        upper = 100
    else:
        lower = key_val*10
        upper = (key_val+1)*10
    children = df[(df[key_col]>=lower) & (df[key_col]< upper)].fillna('')
    children['Title'] = children[key_col].astype(str) + ": " + children['Title'] 
    return children



def get_children_keys(key_val, df, key_col='Code'):
    children = get_children(key_val, df, key_col)
    return list(children[key_col])



def create_streamlit_tree(df, 
                          node = {
                                    'label': 'NAICS 2022',
                                    'value': 0,
                                    'description': 'Categorisation tree for NAICS 2022 industry classifications'
                                }, 
                          key_col = 'Code',
                          level = 0,
                          max_level = 20):
    """
    A function creating a list containing tree nodes and their children.
    The list is built up recursively starting from the given root node, and filling in the respective children nodes as follows:
     
    A node is a dict which has the following keys: 
        'value' : the unique identifier of the node. integer
        'label' : the short description of the node. string
        'description' : a longer description of the node. string
        'children' : a list nodes (or missing if the node has no children) 
    The children of a node can be found by calling the function get_children(key_val, df, key_col), 
    where key_val is the value of the node for which we are looking for the children, key_col is the name of the column containing the keys. 
    This function returns the rows of df that correspond to the children of node key_val.
    

    Args:
        df : a data frame containing the data of all of the nodes of the tree. 
            Each row contains the data of a node of the tree. 
            df has columns ['Code', 'Title', 'Description'], where 'Code' corresponds to 'value' of the nodes, 'Title' to 'label', and 'Description' to 'description'.
        node : the current root node
    """
    
    # get a list of dicts for the children        
    children = get_children(node['value'], df, key_col) \
        .rename(columns = {'Code':'value', 'Title':'label', 'Description': 'description'}) \
        .fillna('') \
        .to_dict(orient='records')

    # recursion magic - that's why trees are cool
    if (len(children)>0) & (level < max_level):
        node['children'] = [create_streamlit_tree(df, child, key_col, level+1, max_level) for child in children]
    return node



def get_NAICS_df():
    
    cat_filepath = "https://www.census.gov/naics/2022NAICS/2022_NAICS_Descriptions.xlsx"
    df = pd.read_excel(cat_filepath)
    df = clean_up_2022_NAICS_Descriptions(df)
    return df



def get_NAICS_streamlit(level = 0, max_level = 20):
    df = get_NAICS_df()
    return create_streamlit_tree(df, level=level, max_level=max_level)




# example usage

if __name__ == "__main__":
    df = get_NAICS_df()
    