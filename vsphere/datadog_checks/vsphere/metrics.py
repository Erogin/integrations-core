# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
from pyVmomi import vim

# https://code.vmware.com/apis/358/vsphere/doc/cpu_counters.html

# Set of metrics that are emitted as percentages between 0 and 100. For those metrics, we divide the value by 100
# to get a float between 0 and 1.
PERCENT_METRICS = {
    'cpu.capacity.contention.avg',
    'cpu.coreUtilization.avg',
    'cpu.coreUtilization.max',
    'cpu.coreUtilization.min',
    'cpu.coreUtilization.raw',
    'cpu.corecount.contention.avg',
    'cpu.demandEntitlementRatio.latest',
    'cpu.latency.avg',
    'cpu.readiness.avg',
    'cpu.usage.avg',
    'cpu.usage.max',
    'cpu.usage.min',
    'cpu.usage.raw',
    'cpu.utilization.avg',
    'cpu.utilization.max',
    'cpu.utilization.min',
    'cpu.utilization.raw',
    'datastore.siocActiveTimePercentage.avg',
    'disk.capacity.contention.avg',
    'disk.scsiReservationCnflctsPct.avg',
    'gpu.mem.usage.avg',
    'gpu.mem.usage.max',
    'gpu.mem.usage.min',
    'gpu.mem.usage.raw',
    'gpu.utilization.avg',
    'gpu.utilization.max',
    'gpu.utilization.min',
    'gpu.utilization.raw',
    'mem.capacity.contention.avg',
    'mem.latency.avg',
    'mem.reservedCapacityPct.avg',
    'mem.usage.avg',
    'mem.usage.max',
    'mem.usage.min',
    'mem.usage.raw',
    'mem.vmfs.pbc.capMissRatio.latest',
    'power.capacity.usagePct.avg',
    'rescpu.actav1.latest',
    'rescpu.actav15.latest',
    'rescpu.actav5.latest',
    'rescpu.actpk1.latest',
    'rescpu.actpk15.latest',
    'rescpu.actpk5.latest',
    'rescpu.maxLimited1.latest',
    'rescpu.maxLimited15.latest',
    'rescpu.maxLimited5.latest',
    'rescpu.runav1.latest',
    'rescpu.runav15.latest',
    'rescpu.runav5.latest',
    'rescpu.runpk1.latest',
    'rescpu.runpk15.latest',
    'rescpu.runpk5.latest',
    'storageAdapter.OIOsPct.avg',
    'sys.diskUsage.latest',
    'sys.resourceCpuAct1.latest',
    'sys.resourceCpuAct5.latest',
    'sys.resourceCpuMaxLimited1.latest',
    'sys.resourceCpuMaxLimited5.latest',
    'sys.resourceCpuRun1.latest',
    'sys.resourceCpuRun5.latest',
    'vcResources.priviledgedcpuusage.avg',
    'vcResources.processcpuusage.avg',
    'vcResources.systemcpuusage.avg',
    'vcResources.systemnetusage.avg',
    'vcResources.usercpuusage.avg',
    'vsanDomObj.readCacheHitRate.latest',
}

# All metrics that can be collected from VirtualMachines.
# The table maps a dd-formatted metric_name to a tuple containing:
# (collection_level, per_instance_collection_level, (optional)is_available_per_instance)
VM_METRICS = {
    'cpu.costop.sum': (2, 3),
    'cpu.demand.avg': (2, 3),
    'cpu.demandEntitlementRatio.latest': (4, 4),
    'cpu.entitlement.latest': (2, 3),
    'cpu.idle.sum': (2, 3, True),
    'cpu.latency.avg': (2, 3),
    'cpu.maxlimited.sum': (2, 3, True),
    'cpu.overlap.sum': (3, 3, True),
    'cpu.readiness.avg': (4, 4),
    'cpu.ready.sum': (1, 3),
    'cpu.run.sum': (2, 3, True),
    'cpu.swapwait.sum': (3, 3),
    'cpu.system.sum': (3, 3, True),
    'cpu.usage.avg': (1, 3, True),
    'cpu.usage.max': (4, 4, True),
    'cpu.usage.min': (4, 4, True),
    'cpu.usage.raw': (4, 4, True),
    'cpu.usagemhz.avg': (1, 3),
    'cpu.usagemhz.max': (4, 4),
    'cpu.usagemhz.min': (4, 4),
    'cpu.usagemhz.raw': (4, 4),
    'cpu.used.sum': (3, 3, True),
    'cpu.wait.sum': (3, 3),
    'datastore.maxTotalLatency.latest': (3, 3),
    'datastore.numberReadAveraged.avg': (1, 3),
    'datastore.numberWriteAveraged.avg': (1, 3),
    'datastore.read.avg': (2, 2, True),
    'datastore.totalReadLatency.avg': (1, 3, True),
    'datastore.totalWriteLatency.avg': (1, 3, True),
    'datastore.write.avg': (2, 2, True),
    'disk.busResets.sum': (2, 3, True),
    'disk.commands.sum': (2, 3, True),
    'disk.commandsAborted.sum': (2, 3, True),
    'disk.commandsAveraged.avg': (2, 3, True),
    'disk.maxTotalLatency.latest': (1, 3),
    'disk.numberRead.sum': (3, 3, True),
    'disk.numberReadAveraged.avg': (1, 3),
    'disk.numberWrite.sum': (3, 3, True),
    'disk.numberWriteAveraged.avg': (1, 3),
    'disk.read.avg': (2, 3, True),
    'disk.usage.avg': (1, 3),
    'disk.usage.max': (4, 4),
    'disk.usage.min': (4, 4),
    'disk.usage.raw': (4, 4),
    'disk.write.avg': (2, 3, True),
    'hbr.hbrNetRx.avg': (4, 4),
    'hbr.hbrNetTx.avg': (4, 4),
    'mem.active.avg': (2, 3),
    'mem.active.max': (4, 4),
    'mem.active.min': (4, 4),
    'mem.active.raw': (4, 4),
    'mem.activewrite.avg': (2, 3),
    'mem.compressed.avg': (2, 3),
    'mem.compressionRate.avg': (2, 3),
    'mem.consumed.avg': (1, 3),
    'mem.consumed.max': (4, 4),
    'mem.consumed.min': (4, 4),
    'mem.consumed.raw': (4, 4),
    'mem.decompressionRate.avg': (2, 3),
    'mem.entitlement.avg': (2, 3),
    'mem.granted.avg': (2, 3),
    'mem.granted.max': (4, 4),
    'mem.granted.min': (4, 4),
    'mem.granted.raw': (4, 4),
    'mem.latency.avg': (2, 3),
    'mem.llSwapInRate.avg': (2, 3),
    'mem.llSwapOutRate.avg': (2, 3),
    'mem.llSwapUsed.avg': (4, 4),
    'mem.llSwapUsed.max': (4, 4),
    'mem.llSwapUsed.min': (4, 4),
    'mem.llSwapUsed.raw': (4, 4),
    'mem.overhead.avg': (1, 1),
    'mem.overhead.max': (4, 4),
    'mem.overhead.min': (4, 4),
    'mem.overhead.raw': (4, 4),
    'mem.overheadMax.avg': (2, 3),
    'mem.overheadTouched.avg': (4, 4),
    'mem.shared.avg': (2, 3),
    'mem.shared.max': (4, 4),
    'mem.shared.min': (4, 4),
    'mem.shared.raw': (4, 4),
    'mem.swapin.avg': (2, 3),
    'mem.swapin.max': (4, 4),
    'mem.swapin.min': (4, 4),
    'mem.swapin.raw': (4, 4),
    'mem.swapinRate.avg': (1, 3),
    'mem.swapout.avg': (2, 3),
    'mem.swapout.max': (4, 4),
    'mem.swapout.min': (4, 4),
    'mem.swapout.raw': (4, 4),
    'mem.swapoutRate.avg': (1, 3),
    'mem.swapped.avg': (2, 3),
    'mem.swapped.max': (4, 4),
    'mem.swapped.min': (4, 4),
    'mem.swapped.raw': (4, 4),
    'mem.swaptarget.avg': (2, 3),
    'mem.swaptarget.max': (4, 4),
    'mem.swaptarget.min': (4, 4),
    'mem.swaptarget.raw': (4, 4),
    'mem.usage.avg': (1, 3),
    'mem.usage.max': (4, 4),
    'mem.usage.min': (4, 4),
    'mem.usage.raw': (4, 4),
    'mem.vmmemctl.avg': (1, 3),
    'mem.vmmemctl.max': (4, 4),
    'mem.vmmemctl.min': (4, 4),
    'mem.vmmemctl.raw': (4, 4),
    'mem.vmmemctltarget.avg': (2, 3),
    'mem.vmmemctltarget.max': (4, 4),
    'mem.vmmemctltarget.min': (4, 4),
    'mem.vmmemctltarget.raw': (4, 4),
    'mem.zero.avg': (2, 3),
    'mem.zero.max': (4, 4),
    'mem.zero.min': (4, 4),
    'mem.zero.raw': (4, 4),
    'mem.zipSaved.latest': (2, 3),
    'mem.zipped.latest': (2, 3),
    'net.broadcastRx.sum': (2, 3, True),
    'net.broadcastTx.sum': (2, 3, True),
    'net.bytesRx.avg': (2, 3, True),
    'net.bytesTx.avg': (2, 3, True),
    'net.droppedRx.sum': (2, 3, True),
    'net.droppedTx.sum': (2, 3, True),
    'net.multicastRx.sum': (2, 3, True),
    'net.multicastTx.sum': (2, 3, True),
    'net.packetsRx.sum': (2, 3, True),
    'net.packetsTx.sum': (2, 3, True),
    'net.pnicBytesRx.avg': (4, 4, True),
    'net.pnicBytesTx.avg': (4, 4, True),
    'net.received.avg': (2, 3, True),
    'net.transmitted.avg': (2, 3, True),
    'net.usage.avg': (1, 3, True),
    'net.usage.max': (4, 4, True),
    'net.usage.min': (4, 4, True),
    'net.usage.raw': (4, 4, True),
    'power.energy.sum': (3, 3),
    'power.power.avg': (2, 3),
    'rescpu.actav1.latest': (3, 3),
    'rescpu.actav15.latest': (3, 3),
    'rescpu.actav5.latest': (3, 3),
    'rescpu.actpk1.latest': (3, 3),
    'rescpu.actpk15.latest': (3, 3),
    'rescpu.actpk5.latest': (3, 3),
    'rescpu.maxLimited1.latest': (3, 3),
    'rescpu.maxLimited15.latest': (3, 3),
    'rescpu.maxLimited5.latest': (3, 3),
    'rescpu.runav1.latest': (3, 3),
    'rescpu.runav15.latest': (3, 3),
    'rescpu.runav5.latest': (3, 3),
    'rescpu.runpk1.latest': (3, 3),
    'rescpu.runpk15.latest': (3, 3),
    'rescpu.runpk5.latest': (3, 3),
    'rescpu.sampleCount.latest': (3, 3),
    'rescpu.samplePeriod.latest': (3, 3),
    'sys.heartbeat.latest': (4, 4),
    'sys.heartbeat.sum': (1, 3),
    'sys.osUptime.latest': (4, 4),
    'sys.uptime.latest': (1, 3),
    'virtualDisk.busResets.sum': (2, 4, True),
    'virtualDisk.commandsAborted.sum': (2, 4, True),
    'virtualDisk.largeSeeks.latest': (4, 4, True),
    'virtualDisk.mediumSeeks.latest': (4, 4, True),
    'virtualDisk.numberReadAveraged.avg': (1, 3, True),
    'virtualDisk.numberWriteAveraged.avg': (1, 3, True),
    'virtualDisk.read.avg': (2, 2, True),
    'virtualDisk.readIOSize.latest': (4, 4, True),
    'virtualDisk.readLatencyUS.latest': (4, 4, True),
    'virtualDisk.readLoadMetric.latest': (2, 2, True),
    'virtualDisk.readOIO.latest': (2, 2, True),
    'virtualDisk.smallSeeks.latest': (4, 4, True),
    'virtualDisk.totalReadLatency.avg': (1, 3, True),
    'virtualDisk.totalWriteLatency.avg': (1, 3, True),
    'virtualDisk.write.avg': (2, 2, True),
    'virtualDisk.writeIOSize.latest': (4, 4, True),
    'virtualDisk.writeLatencyUS.latest': (4, 4, True),
    'virtualDisk.writeLoadMetric.latest': (2, 2, True),
    'virtualDisk.writeOIO.latest': (2, 2, True),
}

# All metrics that can be collected from ESXi Hosts.
# The table maps a dd-formatted metric_name to a tuple containing:
# (collection_level, per_instance_collection_level, (optional)is_available_per_instance)
HOST_METRICS = {
    'cpu.coreUtilization.avg': (2, 3, True),
    'cpu.coreUtilization.max': (4, 4, True),
    'cpu.coreUtilization.min': (4, 4, True),
    'cpu.coreUtilization.raw': (4, 4, True),
    'cpu.costop.sum': (2, 3),
    'cpu.demand.avg': (2, 3),
    'cpu.idle.sum': (2, 3, True),
    'cpu.latency.avg': (2, 3),
    'cpu.readiness.avg': (4, 4),
    'cpu.ready.sum': (1, 3),
    'cpu.reservedCapacity.avg': (2, 3),
    'cpu.swapwait.sum': (3, 3),
    'cpu.totalCapacity.avg': (2, 3),
    'cpu.usage.avg': (1, 3, True),
    'cpu.usage.max': (4, 4, True),
    'cpu.usage.min': (4, 4, True),
    'cpu.usage.raw': (4, 4, True),
    'cpu.usagemhz.avg': (1, 3),
    'cpu.usagemhz.max': (4, 4),
    'cpu.usagemhz.min': (4, 4),
    'cpu.usagemhz.raw': (4, 4),
    'cpu.used.sum': (3, 3, True),
    'cpu.utilization.avg': (2, 3, True),
    'cpu.utilization.max': (4, 4, True),
    'cpu.utilization.min': (4, 4, True),
    'cpu.utilization.raw': (4, 4, True),
    'cpu.wait.sum': (3, 3),
    'datastore.datastoreIops.avg': (1, 3, True),
    'datastore.datastoreMaxQueueDepth.latest': (1, 3, True),
    'datastore.datastoreNormalReadLatency.latest': (2, 2, True),
    'datastore.datastoreNormalWriteLatency.latest': (2, 2, True),
    'datastore.datastoreReadBytes.latest': (2, 2, True),
    'datastore.datastoreReadIops.latest': (1, 3, True),
    'datastore.datastoreReadLoadMetric.latest': (4, 4, True),
    'datastore.datastoreReadOIO.latest': (1, 3, True),
    'datastore.datastoreVMObservedLatency.latest': (1, 3, True),
    'datastore.datastoreWriteBytes.latest': (2, 2, True),
    'datastore.datastoreWriteIops.latest': (1, 3, True),
    'datastore.datastoreWriteLoadMetric.latest': (4, 4, True),
    'datastore.datastoreWriteOIO.latest': (1, 3, True),
    'datastore.maxTotalLatency.latest': (3, 3),
    'datastore.numberReadAveraged.avg': (1, 3),
    'datastore.numberWriteAveraged.avg': (1, 3),
    'datastore.read.avg': (2, 2, True),
    'datastore.siocActiveTimePercentage.avg': (1, 3, True),
    'datastore.sizeNormalizedDatastoreLatency.avg': (1, 3, True),
    'datastore.totalReadLatency.avg': (1, 3, True),
    'datastore.totalWriteLatency.avg': (1, 3, True),
    'datastore.write.avg': (2, 2, True),
    'disk.busResets.sum': (2, 3, True),
    'disk.commands.sum': (2, 3, True),
    'disk.commandsAborted.sum': (2, 3, True),
    'disk.commandsAveraged.avg': (2, 3, True),
    'disk.deviceLatency.avg': (1, 3, True),
    'disk.deviceReadLatency.avg': (2, 3, True),
    'disk.deviceWriteLatency.avg': (2, 3, True),
    'disk.kernelLatency.avg': (2, 3, True),
    'disk.kernelReadLatency.avg': (2, 3, True),
    'disk.kernelWriteLatency.avg': (2, 3, True),
    'disk.maxQueueDepth.avg': (1, 3, True),
    'disk.maxTotalLatency.latest': (1, 3),
    'disk.numberRead.sum': (3, 3, True),
    'disk.numberReadAveraged.avg': (1, 3),
    'disk.numberWrite.sum': (3, 3, True),
    'disk.numberWriteAveraged.avg': (1, 3),
    'disk.queueLatency.avg': (2, 3, True),
    'disk.queueReadLatency.avg': (2, 3, True),
    'disk.queueWriteLatency.avg': (2, 3, True),
    'disk.read.avg': (2, 3, True),
    'disk.scsiReservationCnflctsPct.avg': (4, 4, True),
    'disk.scsiReservationConflicts.sum': (2, 2, True),
    'disk.totalLatency.avg': (3, 3, True),
    'disk.totalReadLatency.avg': (2, 3, True),
    'disk.totalWriteLatency.avg': (2, 3, True),
    'disk.usage.avg': (1, 3),
    'disk.usage.max': (4, 4),
    'disk.usage.min': (4, 4),
    'disk.usage.raw': (4, 4),
    'disk.write.avg': (2, 3, True),
    'hbr.hbrNetRx.avg': (4, 4),
    'hbr.hbrNetTx.avg': (4, 4),
    'hbr.hbrNumVms.avg': (4, 4),
    'mem.active.avg': (2, 3),
    'mem.active.max': (4, 4),
    'mem.active.min': (4, 4),
    'mem.active.raw': (4, 4),
    'mem.activewrite.avg': (2, 3),
    'mem.compressed.avg': (2, 3),
    'mem.compressionRate.avg': (2, 3),
    'mem.consumed.avg': (1, 3),
    'mem.consumed.max': (4, 4),
    'mem.consumed.min': (4, 4),
    'mem.consumed.raw': (4, 4),
    'mem.consumed.userworlds.avg': (2, 4),
    'mem.consumed.vms.avg': (2, 4),
    'mem.decompressionRate.avg': (2, 3),
    'mem.granted.avg': (2, 3),
    'mem.granted.max': (4, 4),
    'mem.granted.min': (4, 4),
    'mem.granted.raw': (4, 4),
    'mem.heap.avg': (4, 4),
    'mem.heap.max': (4, 4),
    'mem.heap.min': (4, 4),
    'mem.heap.raw': (4, 4),
    'mem.heapfree.avg': (4, 4),
    'mem.heapfree.max': (4, 4),
    'mem.heapfree.min': (4, 4),
    'mem.heapfree.raw': (4, 4),
    'mem.latency.avg': (2, 3),
    'mem.llSwapIn.avg': (4, 4),
    'mem.llSwapIn.max': (4, 4),
    'mem.llSwapIn.min': (4, 4),
    'mem.llSwapIn.raw': (4, 4),
    'mem.llSwapInRate.avg': (2, 3),
    'mem.llSwapOut.avg': (4, 4),
    'mem.llSwapOut.max': (4, 4),
    'mem.llSwapOut.min': (4, 4),
    'mem.llSwapOut.raw': (4, 4),
    'mem.llSwapOutRate.avg': (2, 3),
    'mem.llSwapUsed.avg': (4, 4),
    'mem.llSwapUsed.max': (4, 4),
    'mem.llSwapUsed.min': (4, 4),
    'mem.llSwapUsed.raw': (4, 4),
    'mem.lowfreethreshold.avg': (2, 3),
    'mem.overhead.avg': (1, 1),
    'mem.overhead.max': (4, 4),
    'mem.overhead.min': (4, 4),
    'mem.overhead.raw': (4, 4),
    'mem.reservedCapacity.avg': (2, 3),
    'mem.shared.avg': (2, 3),
    'mem.shared.max': (4, 4),
    'mem.shared.min': (4, 4),
    'mem.shared.raw': (4, 4),
    'mem.sharedcommon.avg': (2, 3),
    'mem.sharedcommon.max': (4, 4),
    'mem.sharedcommon.min': (4, 4),
    'mem.sharedcommon.raw': (4, 4),
    'mem.state.latest': (2, 3),
    'mem.swapin.avg': (2, 3),
    'mem.swapin.max': (4, 4),
    'mem.swapin.min': (4, 4),
    'mem.swapin.raw': (4, 4),
    'mem.swapinRate.avg': (1, 3),
    'mem.swapout.avg': (2, 3),
    'mem.swapout.max': (4, 4),
    'mem.swapout.min': (4, 4),
    'mem.swapout.raw': (4, 4),
    'mem.swapoutRate.avg': (1, 3),
    'mem.swapused.avg': (2, 3),
    'mem.swapused.max': (4, 4),
    'mem.swapused.min': (4, 4),
    'mem.swapused.raw': (4, 4),
    'mem.sysUsage.avg': (2, 3),
    'mem.sysUsage.max': (4, 4),
    'mem.sysUsage.min': (4, 4),
    'mem.sysUsage.raw': (4, 4),
    'mem.totalCapacity.avg': (2, 3),
    'mem.unreserved.avg': (2, 3),
    'mem.unreserved.max': (4, 4),
    'mem.unreserved.min': (4, 4),
    'mem.unreserved.raw': (4, 4),
    'mem.usage.avg': (1, 3),
    'mem.usage.max': (4, 4),
    'mem.usage.min': (4, 4),
    'mem.usage.raw': (4, 4),
    'mem.vmfs.pbc.capMissRatio.latest': (4, 4),
    'mem.vmfs.pbc.overhead.latest': (4, 4),
    'mem.vmfs.pbc.size.latest': (4, 4),
    'mem.vmfs.pbc.sizeMax.latest': (4, 4),
    'mem.vmfs.pbc.workingSet.latest': (4, 4),
    'mem.vmfs.pbc.workingSetMax.latest': (4, 4),
    'mem.vmmemctl.avg': (1, 3),
    'mem.vmmemctl.max': (4, 4),
    'mem.vmmemctl.min': (4, 4),
    'mem.vmmemctl.raw': (4, 4),
    'mem.zero.avg': (2, 3),
    'mem.zero.max': (4, 4),
    'mem.zero.min': (4, 4),
    'mem.zero.raw': (4, 4),
    'net.broadcastRx.sum': (2, 3, True),
    'net.broadcastTx.sum': (2, 3, True),
    'net.bytesRx.avg': (2, 3, True),
    'net.bytesTx.avg': (2, 3, True),
    'net.droppedRx.sum': (2, 3, True),
    'net.droppedTx.sum': (2, 3, True),
    'net.errorsRx.sum': (2, 3, True),
    'net.errorsTx.sum': (2, 3, True),
    'net.multicastRx.sum': (2, 3, True),
    'net.multicastTx.sum': (2, 3, True),
    'net.packetsRx.sum': (2, 3, True),
    'net.packetsTx.sum': (2, 3, True),
    'net.received.avg': (2, 3, True),
    'net.transmitted.avg': (2, 3, True),
    'net.unknownProtos.sum': (2, 3, True),
    'net.usage.avg': (1, 3, True),
    'net.usage.max': (4, 4, True),
    'net.usage.min': (4, 4, True),
    'net.usage.raw': (4, 4, True),
    'power.energy.sum': (3, 3),
    'power.power.avg': (2, 3),
    'power.powerCap.avg': (3, 3),
    'rescpu.actav1.latest': (3, 3),
    'rescpu.actav15.latest': (3, 3),
    'rescpu.actav5.latest': (3, 3),
    'rescpu.actpk1.latest': (3, 3),
    'rescpu.actpk15.latest': (3, 3),
    'rescpu.actpk5.latest': (3, 3),
    'rescpu.maxLimited1.latest': (3, 3),
    'rescpu.maxLimited15.latest': (3, 3),
    'rescpu.maxLimited5.latest': (3, 3),
    'rescpu.runav1.latest': (3, 3),
    'rescpu.runav15.latest': (3, 3),
    'rescpu.runav5.latest': (3, 3),
    'rescpu.runpk1.latest': (3, 3),
    'rescpu.runpk15.latest': (3, 3),
    'rescpu.runpk5.latest': (3, 3),
    'rescpu.sampleCount.latest': (3, 3),
    'rescpu.samplePeriod.latest': (3, 3),
    'storageAdapter.commandsAveraged.avg': (2, 2, True),
    'storageAdapter.maxTotalLatency.latest': (3, 3),
    'storageAdapter.numberReadAveraged.avg': (2, 2, True),
    'storageAdapter.numberWriteAveraged.avg': (2, 2, True),
    'storageAdapter.outstandingIOs.avg': (2, 2, True),
    'storageAdapter.queueDepth.avg': (2, 2, True),
    'storageAdapter.queueLatency.avg': (2, 2, True),
    'storageAdapter.queued.avg': (2, 2, True),
    'storageAdapter.read.avg': (2, 2, True),
    'storageAdapter.totalReadLatency.avg': (2, 2, True),
    'storageAdapter.totalWriteLatency.avg': (2, 2, True),
    'storageAdapter.write.avg': (2, 2, True),
    'storagePath.busResets.sum': (2, 3, True),
    'storagePath.commandsAborted.sum': (2, 3, True),
    'storagePath.commandsAveraged.avg': (3, 3, True),
    'storagePath.maxTotalLatency.latest': (3, 3),
    'storagePath.numberReadAveraged.avg': (3, 3, True),
    'storagePath.numberWriteAveraged.avg': (3, 3, True),
    'storagePath.read.avg': (3, 3, True),
    'storagePath.totalReadLatency.avg': (3, 3, True),
    'storagePath.totalWriteLatency.avg': (3, 3, True),
    'storagePath.write.avg': (3, 3, True),
    'sys.resourceCpuAct1.latest': (3, 3, True),
    'sys.resourceCpuAct5.latest': (3, 3, True),
    'sys.resourceCpuAllocMax.latest': (3, 3, True),
    'sys.resourceCpuAllocMin.latest': (3, 3, True),
    'sys.resourceCpuAllocShares.latest': (3, 3, True),
    'sys.resourceCpuMaxLimited1.latest': (3, 3, True),
    'sys.resourceCpuMaxLimited5.latest': (3, 3, True),
    'sys.resourceCpuRun1.latest': (3, 3, True),
    'sys.resourceCpuRun5.latest': (3, 3, True),
    'sys.resourceCpuUsage.avg': (3, 3, True),
    'sys.resourceCpuUsage.max': (4, 4, True),
    'sys.resourceCpuUsage.min': (4, 4, True),
    'sys.resourceCpuUsage.raw': (4, 4, True),
    'sys.resourceFdUsage.latest': (4, 4, True),
    'sys.resourceMemAllocMax.latest': (3, 3, True),
    'sys.resourceMemAllocMin.latest': (3, 3, True),
    'sys.resourceMemAllocShares.latest': (3, 3, True),
    'sys.resourceMemConsumed.latest': (4, 4, True),
    'sys.resourceMemCow.latest': (3, 3, True),
    'sys.resourceMemMapped.latest': (3, 3, True),
    'sys.resourceMemOverhead.latest': (3, 3, True),
    'sys.resourceMemShared.latest': (3, 3, True),
    'sys.resourceMemSwapped.latest': (3, 3, True),
    'sys.resourceMemTouched.latest': (3, 3, True),
    'sys.resourceMemZero.latest': (3, 3, True),
    'sys.uptime.latest': (1, 3),
    'virtualDisk.busResets.sum': (2, 4, True),
    'virtualDisk.commandsAborted.sum': (2, 4, True),
}

# All metrics that can be collected from Datastores.
# The table maps a dd-formatted metric_name to a tuple containing:
# (collection_level, per_instance_collection_level, (optional)is_available_per_instance)
DATASTORE_METRICS = {
    'datastore.busResets.sum': (2, 2, True),
    'datastore.commandsAborted.sum': (2, 2, True),
    'datastore.numberReadAveraged.avg': (1, 3),
    'datastore.numberWriteAveraged.avg': (1, 3),
    'datastore.throughput.contention.avg': (4, 4, True),
    'datastore.throughput.usage.avg': (4, 4, True),
    'disk.busResets.sum': (2, 3, True),
    'disk.capacity.contention.avg': (4, 4),
    'disk.capacity.latest': (1, 3),
    'disk.capacity.provisioned.avg': (4, 4),
    'disk.capacity.usage.avg': (4, 4, True),
    'disk.numberReadAveraged.avg': (1, 3),
    'disk.numberWriteAveraged.avg': (1, 3),
    'disk.provisioned.latest': (1, 1, True),
    'disk.unshared.latest': (1, 1, True),
    'disk.used.latest': (1, 1, True),
}

# All metrics that can be collected from Datacenters.
# The table maps a dd-formatted metric_name to a tuple containing:
# (collection_level, per_instance_collection_level, (optional)is_available_per_instance)
DATACENTER_METRICS = {
    'vmop.numChangeDS.latest': (1, 3),
    'vmop.numChangeHost.latest': (1, 3),
    'vmop.numChangeHostDS.latest': (1, 3),
    'vmop.numClone.latest': (1, 3),
    'vmop.numCreate.latest': (1, 3),
    'vmop.numDeploy.latest': (1, 3),
    'vmop.numDestroy.latest': (1, 3),
    'vmop.numPoweroff.latest': (1, 3),
    'vmop.numPoweron.latest': (1, 3),
    'vmop.numRebootGuest.latest': (1, 3),
    'vmop.numReconfigure.latest': (1, 3),
    'vmop.numRegister.latest': (1, 3),
    'vmop.numReset.latest': (1, 3),
    'vmop.numSVMotion.latest': (1, 3),
    'vmop.numShutdownGuest.latest': (1, 3),
    'vmop.numStandbyGuest.latest': (1, 3),
    'vmop.numSuspend.latest': (1, 3),
    'vmop.numUnregister.latest': (1, 3),
    'vmop.numVMotion.latest': (1, 3),
    'vmop.numXVMotion.latest': (1, 3),
}

# All metrics that can be collected from Clusters.
# The table maps a dd-formatted metric_name to a tuple containing:
# (collection_level, per_instance_collection_level, (optional)is_available_per_instance)
CLUSTER_METRICS = {
    # clusterServices are only available for DRS and HA clusters, and are causing errors. Let's deactivate for now
    # but they were collected before so investigate why
    'clusterServices.cpufairness.latest': (1, 3),
    'clusterServices.effectivecpu.avg': (1, 3),
    'clusterServices.effectivemem.avg': (1, 3),
    'clusterServices.failover.latest': (1, 3),
    'clusterServices.memfairness.latest': (1, 3),
    'cpu.totalmhz.avg': (1, 3),
    'cpu.usage.avg': (1, 3, True),
    'cpu.usagemhz.avg': (1, 3),
    'mem.consumed.avg': (1, 3),
    'mem.overhead.avg': (1, 1),
    'mem.totalmb.avg': (1, 3),
    'mem.usage.avg': (1, 3),
    'mem.vmmemctl.avg': (1, 3),
    'vmop.numChangeDS.latest': (1, 3),
    'vmop.numChangeHost.latest': (1, 3),
    'vmop.numChangeHostDS.latest': (1, 3),
    'vmop.numClone.latest': (1, 3),
    'vmop.numCreate.latest': (1, 3),
    'vmop.numDeploy.latest': (1, 3),
    'vmop.numDestroy.latest': (1, 3),
    'vmop.numPoweroff.latest': (1, 3),
    'vmop.numPoweron.latest': (1, 3),
    'vmop.numRebootGuest.latest': (1, 3),
    'vmop.numReconfigure.latest': (1, 3),
    'vmop.numRegister.latest': (1, 3),
    'vmop.numReset.latest': (1, 3),
    'vmop.numSVMotion.latest': (1, 3),
    'vmop.numShutdownGuest.latest': (1, 3),
    'vmop.numStandbyGuest.latest': (1, 3),
    'vmop.numSuspend.latest': (1, 3),
    'vmop.numUnregister.latest': (1, 3),
    'vmop.numVMotion.latest': (1, 3),
    'vmop.numXVMotion.latest': (1, 3),
}

ALLOWED_METRICS_FOR_MOR = {
    vim.VirtualMachine: VM_METRICS,
    vim.HostSystem: HOST_METRICS,
    vim.Datacenter: DATACENTER_METRICS,
    vim.Datastore: DATASTORE_METRICS,
    vim.ClusterComputeResource: CLUSTER_METRICS,
}
