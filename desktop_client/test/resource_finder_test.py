from ..src.utils.resource import ResourceFinder


def test_running_path():
    resource_finder = ResourceFinder()
    assert resource_finder is not None

    path = resource_finder.get_running_root()
    assert path is not None


def test_find_this_module():
    resource_finder = ResourceFinder()
    assert resource_finder is not None

    print(f'--> File path {__file__}')
    print(f'--> File {__name__.split('.')[len(__name__.split('.')) - 1]}.py')
    path = resource_finder.find_resource_file(
        f'{__name__.split('.')[len(__name__.split('.')) - 1]}.py')
    assert path is not None
    assert str(path) == __file__
