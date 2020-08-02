## 进一步的改进

希望能够在 `tensorboard`上打印出loss，f1_score, recall, precision的变化。

还是接上一次的研究

如果希望能够在tensorboard中显示出evaluate的过程中的指标的变化，但是参照了多种网上的方法都没有实现。按照网上的说法：

>  In the new versions of Tensorflow, this works if you pass the hook to `evaluate`, but not for `train`. For train you only need to define the summaries in `mode_fn` and they will be automatically logged to tensorboard. (Yes, I also feel this is dumb and counterintuitive) – [GPhilo](https://stackoverflow.com/users/3214872/gphilo) [Feb 16 '18 at 11:04](https://stackoverflow.com/questions/45086109/tensorflow-using-tf-summary-with-1-2-estimator-api#comment84654316_45143243) 

train中是直接添加`tf.summary.scale()`的，但是在evaluate中需要使用`summary_hook`

```python
summary_hook = tf.train.SummarySaverHook(
    save_secs=2,
    output_dir=MODEL_DIR,
    scaffold=tf.train.Scaffold(summary_op=tf.summary.merge_all()))

#...

classifier.train(
    input_fn,
    steps=1000,
    hooks=[summary_hook])
```

上述方法经过多次实践后发现行不通

最后换了一种解决方法：

将我们需要保存summary的指标比如说f1_score等指标放到mode_fn 开头进行计算：

```python
def model_fn_builder(bert_config, num_labels, init_checkpoint, learning_rate, num_train_steps,
                     num_warmup_steps, use_one_hot_embeddings):
    '''When define mode_fn, it does not use params from estimator, try to define function
    model_fn_builder, and pass the parameter'''
    def model_fn(features, labels, mode, params):
        '''The 'model_fn' for estimator'''


        tf.logging.info("*** Features ***")
        for name in sorted(features.keys()):
            tf.logging.info(" name = %s, shape = %s" % (name, features[name].shape))

        input_ids = features["input_ids"]
        input_mask = features["input_mask"]
        segment_ids = features["segment_ids"]
        label_ids = features["label_ids"]
        is_real_example=None
        if "is_real_example" in features:
            is_real_example = tf.cast(features["is_real_example"], dtype=tf.float32)
        else:
            is_real_example = tf.ones(tf.shape(label_ids), dtype=tf.float32)

        is_training = (mode == tf.estimator.ModeKeys.TRAIN)

        (total_loss, per_example_loss, predictions, probabilities) = create_model(bert_config, is_training, input_ids,
        input_mask, segment_ids, label_ids, num_labels, use_one_hot_embeddings)

        tvars=tf.trainable_variables()
        initialized_variable_names = {}
        if init_checkpoint:
            (assignment_map, initialized_variable_names
             ) = modeling.get_assignment_map_from_checkpoint(tvars, init_checkpoint)
            tf.train.init_from_checkpoint(init_checkpoint, assignment_map)

        tf.logging.info("*** Trainable Variables ***")
        for var in tvars:
            init_string = ""
            if var.name in initialized_variable_names:
                init_string = ", *INIT_FROM_CKPT*"
            tf.logging.info("  name = %s, shape = %s%s", var.name, var.shape,
                            init_string)

        output_spec = None
        #2020/8/2
        tf.summary.scalar('total_loss1', total_loss)
        recall_out = tf.metrics.recall(labels=label_ids, predictions=predictions, weights=is_real_example)
        tf.summary.scalar('recall_output', recall_out[1])
        '''def metric_fnn(per_example_loss, label_ids, predictions, is_real_example):
            precision = tf.metrics.precision(labels=label_ids, predictions=predictions, weights=is_real_example)
        recall = tf.metrics.recall(labels=label_ids, predictions=predictions, weights=is_real_example)
            f1 = (2 * precision[0] * recall[0] / (precision[0] + recall[0]), recall[1])
            return recall[0]
        recall_output = metric_fnn(per_example_loss, label_ids, predictions, is_real_example)
        tf.summary.scalar('recall_output', recall_output)'''
        #tf.summary.scalar('probability1', probabilities)
        #precision1 = tf.metrics.precision(labels=label_ids, predictions=predictions, weights=is_real_example)
        #tf.summary.scalar('precision1', precision1)
        #merged_summary_op=tf.summary.merge_all()
       # sumay_hook=tf.estimator.SummarySaverHook(save_steps=10, output_dir=FLAGS.data_dir, summary_op=merged_summary_op )
        # 2020/8/2
        if mode == tf.estimator.ModeKeys.TRAIN:

            train_op = optimization.create_optimizer(
                total_loss, learning_rate, num_train_steps, num_warmup_steps, False)

            output_spec = tf.estimator.EstimatorSpec(
                mode=mode,
                loss=total_loss,
                train_op=train_op,
                #2020/8/1
                #2020/8/1
            )

        elif mode == tf.estimator.ModeKeys.EVAL:

            def metric_fn(per_example_loss, label_ids, predictions, is_real_example):
                precision = tf.metrics.precision(labels=label_ids, predictions=predictions, weights=is_real_example)
                recall = tf.metrics.recall(labels=label_ids, predictions=predictions, weights=is_real_example)
                f1 = (2 * precision[0] * recall[0] / (precision[0] + recall[0]), recall[1])
                accuracy = tf.metrics.accuracy(
                    labels=label_ids, predictions=predictions, weights=is_real_example
                )
                loss = tf.metrics.mean(values=per_example_loss, weights=is_real_example)
                #2020/8/2
                #tf.summary.scalar('recall_output', recall[1])
                #tf.summary.scalar('accuracy_output', accuracy[1])
                #2020/8/2
                return {
                    "eval_accuracy": accuracy,
                    "eval_precison": precision,
                    "eval_recall": recall,
                    "eval_f1": f1,
                    "eval_loss": loss,
                }
                #2020/8/1
                #2020/8/1
            eval_metric_ops = metric_fn(per_example_loss, label_ids, predictions, is_real_example)
            #2020/8/2
            #tf.summary.scalar("eval_f1_1", eval_metric_ops['eval_f1'][0])

            #tf.summary.scalar("eval_f1_1", eval_metric_ops['eval_f1'][0])
            #tf.summary.scalar('eval_recall3', eval_metric_ops['eval_recall'])
            #2020/8/2
            output_spec = tf.estimator.EstimatorSpec(
                mode=mode,
                loss=total_loss,
                eval_metric_ops=eval_metric_ops
            )
        else:
            output_spec = tf.estimator.EstimatorSpec(
                mode=mode,
                predictions={
                    "probabilities": probabilities,
                    "predictions": predictions
                }
            )
        #2020/8/2
        #tf.summary.scalar('eval_f1_1', eval_f1)
        #tf.summary.merge_all()
        #2020/8/2
        #2020/8/2
        #tf.summary.merge_all()
        #2020/8/2
        return output_spec

    return model_fn
```

