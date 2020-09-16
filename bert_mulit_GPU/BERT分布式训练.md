# BERT分布式训练

一般情况下，分布式训练主要有两种模式，一种是模型并行，一种是数据并行。模型并行指将模型分散到不同的GPU当中，每个GPU只计算和更新自己负责的参数，这种模型并行主要解决模型参数量过大的问题。数据并行是在多个GPU上运行同样的模型，但是他们的输入数据却不一样，实现更大的batch同时计算，加快模型训练速度。

Tensorflow分布式训练的支持主要是通过tf.distribute.Strategy来实现。现在的Tensorflow分布式库中主要包含五种不同的分布式策略：

- MirroredStrategy
- TPUStrategy
- MultiWorkerMirroredStrategy
- CentralStorageStrategy
- ParameterServerStrategy

**MirroredStrategy**

MirroredStrategy是一种支持多张GPU在同一个机器上的同步训练方法。在训练开始时，Mirrored会在每张卡上复制一份模型，个显卡会收到tf.data.Dataset传来的数据，独立计算梯度，然后采用all-reduce的方法进行同步更新。多个显卡在通信时默认使用Nvidia NCCL进行。

下面是创建MirroredStrategy的最简单方法：

```python3
mirrored_strategy = tf.distribute.MirroredStrategy()
```

这会创建一个MirroredStrategy实例，这个实例会使用对TensorFlow可见的所有GPU，以及使用NCCL作为设备通信的方式。

如果你想只使用机器上的部分GPU，你可以这么做：

```python3
mirrored_strategy = tf.distribute.MirroredStrategy(devices=["/gpu:0","/gpu:1"])
```

如果你想覆盖设备通信方式，可以使用 'cross_device_ops' 参数来申请一个 tf.distribute.CrossDeviceOps 实例。目前，tf.distribute.HierarchicalCopyAllReduce 和 tf.distribute.ReductionToOneDevice 是两种额外选项，而 tf.distribute.NcclAllReduce 是默认的。

```python3
mirrored_strategy = tf.distribute.MirroredStrategy(cross_device_ops=tf.distribute.Hier
```

