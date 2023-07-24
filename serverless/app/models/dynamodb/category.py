from boto3.dynamodb.conditions import Key
from app.models.dynamodb import Base


class Category(Base):
    table_name = 'category'
    public_attrs = [
        'cateId',
        'contentDiv',
        'parentId',
        'parentPath',
        'orderNo',
        'slug',
        'labels',
        'meta',
    ]
    response_attrs = public_attrs + [
        'parents',
        'children',
    ]
    private_attrs = [
        'parentPathOrderNo',
        'contentDivSlug',
    ]
    all_attrs = public_attrs + private_attrs

    CONTENT_DIVS = ['region']

    @classmethod
    def get_children_py_parent_path(self, parent_path):
        cates = self.get_all()

    @classmethod
    def get_one_by_slug(self, cont_div, slug, with_children=False, sort_children=False, is_all_attrs=False):
        keys = {'contentDivSlug': '#'.join([cont_div, slug])}
        cate = self.get_one(keys, 'ContentDivSlug_idx', is_all_attrs)
        if not cate:
            return

        if with_children:
            cate['children'] = []
            parent_path = '/'.join([cate['parentPath'], str(cate['cateId'])])
            keys = {'contentDiv': cont_div, 'parentPath': parent_path}
            children = self.get_all(
                keys, None, 'ContentDivParentPath_idx', is_all_attrs)
            if children:
                if sort_children:
                    cate['children'] = sorted(
                        children, key=lambda d: d['orderNo'])
                else:
                    cate['children'] = children
        return cate
