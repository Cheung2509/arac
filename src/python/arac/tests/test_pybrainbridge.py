#! /usr/bin/env python2.5
# -*- coding: utf-8 -*

"""Unittests for the arac.pybrainbridge module."""


__author__ = 'Justin S Bayer, bayer.justin@googlemail.com'


import copy
import unittest

import scipy

import arac.pybrainbridge as pybrainbridge

from arac.tests.common import TestCase

from pybrain.structure import (
    LinearLayer, 
    BiasUnit,
    SigmoidLayer, 
    GateLayer,
    TanhLayer,
    LSTMLayer,
    SoftmaxLayer,
    PartialSoftmaxLayer,
    IdentityConnection, 
    FullConnection,
    Network,
    RecurrentNetwork,
    FeedForwardNetwork
)


scipy.random.seed(0)


class TestNetworkEquivalence(TestCase):
    
    def two_layer_network(self, net):
        inlayer = SigmoidLayer(2, 'in')
        outlayer = LinearLayer(2, 'out')
        con = FullConnection(inlayer, outlayer)
        con.params[:] = 1, 2, 3, 4
        net.addInputModule(inlayer)
        net.addOutputModule(outlayer)
        net.addConnection(con)
        net.sortModules()
        
    def rec_two_layer_network(self, net):
        inlayer = LinearLayer(2, 'in')
        outlayer = LinearLayer(2, 'out')
        con = IdentityConnection(inlayer, outlayer)
        rcon = IdentityConnection(inlayer, outlayer)
        net.addInputModule(inlayer)
        net.addOutputModule(outlayer)
        net.addConnection(con)
        net.addRecurrentConnection(rcon)
        net.sortModules()
        
    def sliced_connection_network(self, net):
        inlayer = LinearLayer(2, 'in')
        outlayer = LinearLayer(2, 'out')
        con = IdentityConnection(inlayer, outlayer, 
                                 inSliceFrom=0, inSliceTo=1,
                                 outSliceFrom=1, outSliceTo=2,
                                 )
        con = IdentityConnection(inlayer, outlayer, 
                         inSliceFrom=1, inSliceTo=2,
                         outSliceFrom=0, outSliceTo=1,
                         )
        net.addInputModule(inlayer)
        net.addOutputModule(outlayer)
        net.addConnection(con)
        net.sortModules()

    def lstm_network(self, net):
        scipy.random.seed(2)
        i = LinearLayer(1, 'in')
        h = LSTMLayer(2, name='hidden')
        o = LinearLayer(1, 'out')
        b = BiasUnit()
        net.addModule(b)
        net.addOutputModule(o)
        net.addInputModule(i)
        net.addModule(h)
        net.addConnection(FullConnection(i, h))
        net.addConnection(FullConnection(b, h))
        # net.addRecurrentConnection(FullConnection(h, h))
        net.addConnection(FullConnection(h, o))
        net.sortModules()
        net.params[:] = scipy.random.random(18)
        
    def lstm_cell(self, net):
        inpt = LinearLayer(4, 'inpt')
        forgetgate = GateLayer(1, 'forgetgate')
        ingate = GateLayer(1, 'ingate')
        outgate = GateLayer(1, 'outgate')
        state = LinearLayer(1, 'state')
        
        in_to_fg = IdentityConnection(inpt, forgetgate, 
                                      inSliceFrom=0, inSliceTo=1,
                                      outSliceFrom=0, outSliceTo=1,
                                      name='in_to_fg')
        in_to_og = IdentityConnection(inpt, outgate, 
                                      inSliceFrom=1, inSliceTo=2,
                                      outSliceFrom=1, outSliceTo=2,
                                      name='in_to_og')
        in_to_ig = IdentityConnection(inpt, ingate,
                                      inSliceFrom=2, inSliceTo=4,
                                      outSliceFrom=0, outSliceTo=2,
                                      name='in_to_ig')
        fg_to_st = IdentityConnection(forgetgate, state,
                                      name='fg_to_st')
        st_to_fg = IdentityConnection(state, forgetgate, 
                                      outSliceFrom=1, outSliceTo=2,
                                      name='st_to_fg'
                                      )
        st_to_og = IdentityConnection(state, outgate,
                                     outSliceFrom=1, outSliceTo=2,
                                     name='st_to_og'
                                     )
        ig_to_st = IdentityConnection(ingate, state, name='ig_to_st')
        
        net.addInputModule(inpt)
        net.addModule(forgetgate)
        net.addModule(ingate)
        net.addModule(state)
        net.addOutputModule(outgate)
        
        net.addConnection(in_to_fg)
        net.addConnection(in_to_og)
        net.addConnection(in_to_ig)
        net.addConnection(fg_to_st)
        net.addRecurrentConnection(st_to_fg)
        net.addConnection(st_to_og)
        net.addConnection(ig_to_st)
        
        net.sortModules()
        
    def weird_network(self, net):
        bias = BiasUnit(name='bias')
        inlayer = TanhLayer(1, name='input')
        outlayer = TanhLayer(1, name='output')
        gatelayer = GateLayer(1, name='gate')
        con1 = FullConnection(bias, gatelayer, outSliceFrom=0, outSliceTo=1)
        con2 = FullConnection(bias, gatelayer, outSliceFrom=1, outSliceTo=2)
        con3 = FullConnection(inlayer, gatelayer, outSliceFrom=0, outSliceTo=1)
        con4 = FullConnection(inlayer, gatelayer, outSliceFrom=1, outSliceTo=2)
        con5 = FullConnection(gatelayer, outlayer)
        net.addInputModule(inlayer)
        net.addModule(bias)
        net.addModule(gatelayer)
        net.addOutputModule(outlayer)
        net.addConnection(con1)
        net.addConnection(con2)
        net.addConnection(con3)
        net.addConnection(con4)
        net.addConnection(con5)
        net.sortModules()
        net.params[:] = 1, 2, 3, 4, 5
        
    def xor_network(self, net):
        net.addInputModule(LinearLayer(2, name='in'))
        net.addModule(BiasUnit(name='bias'))
        net.addModule(LinearLayer(3, name='hidden'))
        net.addOutputModule(LinearLayer(1, name='out'))
        net.addConnection(FullConnection(net['in'], net['hidden']))
        net.addConnection(FullConnection(net['bias'], net['hidden']))
        net.addConnection(FullConnection(net['hidden'], net['out']))
        net.sortModules()
        scipy.random.seed(1)
        net.params[:] = scipy.random.random((12,))
        
    def rec_three_layer_network(self, net):
        inlayer = TanhLayer(2, 'in')
        hiddenlayer = TanhLayer(hiddensize, 'hidden')
        outlayer = LinearLayer(2, 'out')
        con1 = FullConnection(inlayer, hiddenlayer)
        con2 = FullConnection(hiddenlayer, outlayer)
        net.addInputModule(inlayer)
        net.addModule(hiddenlayer)
        net.addOutputModule(outlayer)
        net.addConnection(con1)
        net.addConnection(con2)
        net.sortModules()
        
    def equivalence_feed_forward(self, builder):
        scipy.random.seed(0)
        runs = 5

        _net = pybrainbridge._FeedForwardNetwork()
        builder(_net)
        net = FeedForwardNetwork()
        builder(net)
        
        for _ in xrange(runs):
            inpt = scipy.random.random(net.indim)
            pybrain_res = net.activate(inpt)
            arac_res = _net.activate(inpt)
            
            # for module in net.modulesSorted:
            #     print module.name
            #     for bn, _ in module.bufferlist:
            #         print getattr(net[module.name], bn)
            #         print getattr(_net[module.name], bn)
            #         print "-" * 5
            #     print "=" * 20
            
            self.assertArrayNear(pybrain_res, arac_res)
            error = scipy.random.random(net.outdim)
            pybrain_res = net.backActivate(error)
            arac_res = _net.backActivate(error)
            self.assertArrayNear(pybrain_res, arac_res)
            if hasattr(_net, '_derivs'):
                self.assertArrayNear(_net.derivs, net.derivs)

    def equivalence_recurrent(self, builder):
        scipy.random.seed(0)
        runs = 10

        _net = pybrainbridge._RecurrentNetwork()
        builder(_net)
        net = RecurrentNetwork()
        builder(net)
        
        for i in xrange(runs):
            inpt = scipy.random.random(net.indim)
            pybrain_res = net.activate(inpt)
            arac_res = _net.activate(inpt)
            self.assertArrayNear(pybrain_res, arac_res)

        for _ in xrange(runs):
            error = scipy.random.random(net.outdim)
            pybrain_res = net.backActivate(error)
            arac_res = _net.backActivate(error)
            self.assertArrayNear(pybrain_res, arac_res)
            if hasattr(_net, '_derivs'):
                self.assertArrayNear(_net.derivs, net.derivs)
                
        net.reset()
        _net.reset()
        self.assert_((_net.inputbuffer == 0.).all())
        
        for _ in xrange(runs):
            inpt = scipy.random.random(net.indim)
            pybrain_res = net.activate(inpt)
            arac_res = _net.activate(inpt)
            self.assertArrayNear(pybrain_res, arac_res)

        for _ in xrange(runs):
            error = scipy.random.random(net.outdim)
            pybrain_res = net.backActivate(error)
            arac_res = _net.backActivate(error)
            self.assertArrayNear(pybrain_res, arac_res)
            if hasattr(_net, '_derivs'):
                self.assertArrayNear(_net.derivs, net.derivs)
                
    def testTwoLayerNetwork(self):
        self.equivalence_feed_forward(self.two_layer_network)

    def testSlicedNetwork(self):
        self.equivalence_feed_forward(self.sliced_connection_network)

    def testRecTwoLayerNetwork(self):
        self.equivalence_recurrent(self.rec_two_layer_network)
        
    def testParametersDerivatives(self):
        rnet = pybrainbridge._RecurrentNetwork()
        self.lstm_network(rnet)
        self.assert_(getattr(rnet, '_derivs', None) is not None)

        fnet = pybrainbridge._FeedForwardNetwork()
        self.two_layer_network(fnet)
        self.assert_(getattr(fnet, '_derivs', None) is not None)
        
    def testTimesteps(self):
        _net = pybrainbridge._RecurrentNetwork()
        self.rec_two_layer_network(_net)
        
        netproxy = _net.proxies[_net]
        inproxy = _net.proxies[_net['in']]
        outproxy = _net.proxies[_net['out']]
        conproxy = _net.proxies[_net.connections[_net['in']][0]]
        rconproxy = _net.proxies[_net.recurrentConns[0]]
        
        proxies = netproxy, inproxy, outproxy, conproxy, rconproxy
        for proxy in proxies:
            self.assertEqual(proxy.get_mode(), 2)
            
        self.assertEqual(_net.offset, 0)
        for proxy in proxies:
            self.assertEqual(proxy.timestep(), 0,
                             "%s has wrong timestep." % proxy)

        _net.activate((0., 0.))
        for proxy in proxies:
            self.assertEqual(proxy.timestep(), 1)

        _net.activate((0., 0.))
        for proxy in proxies:
            self.assertEqual(proxy.timestep(), 2)

        _net.activate((0., 0.))
        for proxy in proxies:
            self.assertEqual(proxy.timestep(), 3)

        _net.backActivate((0., 0.))
        self.assertEqual(_net.offset, 2)
        for proxy in proxies:
            self.assertEqual(proxy.timestep(), 2)

        _net.backActivate((0., 0.))
        self.assertEqual(_net.offset, 1)
        for proxy in proxies:
            self.assertEqual(proxy.timestep(), 1)

        _net.backActivate((0., 0.))
        self.assertEqual(_net.offset, 0)
        for proxy in proxies:
            self.assertEqual(proxy.timestep(), 0)

    def testLstmNetwork(self):
        self.equivalence_recurrent(self.lstm_network)

    def testLstmCell(self):
        self.equivalence_recurrent(self.lstm_cell)

    def testWeirdNetwork(self):
        self.equivalence_feed_forward(self.weird_network)
        self.equivalence_recurrent(self.weird_network)

    def testXorNetwork(self):
        self.equivalence_feed_forward(self.xor_network)
        self.equivalence_recurrent(self.weird_network)
        
    def testCopyable(self):
        net = pybrainbridge._RecurrentNetwork()
        self.lstm_network(net)
        success = False
        e = ""
        try:
            copied = net.copy()
            success = True
        except TypeError, e:
            success = False
        self.assert_(success, e)


if __name__ == "__main__":
    unittest.main()  