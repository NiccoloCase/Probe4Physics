from __future__ import annotations

import os
import unittest
from unittest import mock

from omegaconf import OmegaConf

import run


class ReleaseConfigTests(unittest.TestCase):
    def config(self, name, overrides=()):
        return OmegaConf.to_container(run._compose_config(name, list(overrides)), resolve=True)

    def test_local_paths_and_matching_health_roots(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            mvp = self.config('mvp')
            ip2 = self.config('intphys2')
            health = self.config('health')
        self.assertEqual(mvp['videos_root'], 'data/videos/mvp')
        self.assertEqual(ip2['videos_root'], 'data/videos/intphys2')
        for dataset, config in [('mvp', mvp), ('intphys2', ip2)]:
            self.assertEqual(config['feature_cache']['dir'], f'artifacts/features/{dataset}')
            self.assertEqual(health['features']['datasets'][dataset]['dir'], config['feature_cache']['dir'])

    def test_legacy_environment_and_explicit_overrides_resolve_identically(self):
        legacy = '/scratch-shared/spunzo1/probe4physics'
        env = {'P4P_MVP_VIDEOS_ROOT': f'{legacy}/data/videos/mvp',
               'P4P_MVP_FEATURE_DIR': f'{legacy}/artifacts/features/mvp',
               'P4P_INTPHYS2_FEATURE_DIR': f'{legacy}/artifacts/features/intphys2'}
        with mock.patch.dict(os.environ, env):
            implicit = self.config('mvp')
            explicit = self.config('mvp', [f'videos_root={env["P4P_MVP_VIDEOS_ROOT"]}',
                                           f'feature_cache.dir={env["P4P_MVP_FEATURE_DIR"]}'])
            ip2 = self.config('intphys2')
        self.assertEqual(implicit, explicit)
        self.assertEqual(ip2['feature_cache']['dir'], env['P4P_INTPHYS2_FEATURE_DIR'])
        with mock.patch.dict(os.environ, env):
            config = self.config('mvp', ['videos_root=/override/videos'])
        self.assertEqual(config['videos_root'], '/override/videos')

    def test_health_yaml_loading_resolves_environment_paths(self):
        from experiments.health.run import CONFIGS_DIR, _load_yaml
        with mock.patch.dict(os.environ, {'P4P_MVP_VIDEOS_ROOT': '/health/videos'}):
            self.assertEqual(_load_yaml(CONFIGS_DIR / 'mvp.yaml')['videos_root'], '/health/videos')

    def test_readme_example_configuration_composes(self):
        config = self.config('mvp', ['+backbone.kwargs.variant=vith16_384',
                                    '+backbone.kwargs.checkpoint_path=/example/vith16-384.pth.tar',
                                    'backbone.kwargs.device=cuda', 'probe.name=linear',
                                    'probe.layer=24', 'probe.device=cpu'])
        self.assertEqual(config['probe']['layer'], 24)
        self.assertEqual(config['decode']['num_frames'], 16)
        self.assertEqual(config['split']['ratios'], {'train': .6, 'val': .2, 'test': .2})


if __name__ == '__main__':
    unittest.main()
