const amqp = require('amqplib/callback_api');

console.log('using rabbit url', process.env.AMQP_URL);

amqp.connect(process.env.AMQP_URL, function (err, conn) {
    process.once('SIGINT', () => conn.close());
    if (err) {
        console.log('got error trying amqp connection', err);
    }

    conn.createChannel(function (err, channel) {
        const toNode = 'to_node';

        channel.assertQueue(toNode, { durable: false});
        var fromNode = 'from_node';
        channel.assertQueue(fromNode, { durable: false });


        channel.consume(toNode, function (msg) {
            console.log('passing through message', msg.content.toString());
            channel.publish('', fromNode, msg.content);
        }, { noAck: true });
    });
});
