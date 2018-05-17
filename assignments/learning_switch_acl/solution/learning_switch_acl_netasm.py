# ################################################################################
# ##
# ##  https://github.com/NetASM/NetASM-python
# ##
# ##  File:
# ##        learning_switch.py
# ##
# ##  Project:
# ##        NetASM: A Network Assembly Language for Programmable Dataplanes
# ##
# ##  Author:
# ##        Muhammad Shahbaz
# ##
# ##  Copyright notice:
# ##        Copyright (C) 2014 Princeton University
# ##      Network Operations and Internet Security Lab
# ##
# ##  Licence:
# ##        This file is a part of the NetASM development base package.
# ##
# ##        This file is free code: you can redistribute it and/or modify it under
# ##        the terms of the GNU Lesser General Public License version 2.1 as
# ##        published by the Free Software Foundation.
# ##
# ##        This package is distributed in the hope that it will be useful, but
# ##        WITHOUT ANY WARRANTY; without even the implied warranty of
# ##        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# ##        Lesser General Public License for more details.
# ##
# ##        You should have received a copy of the GNU Lesser General Public
# ##        License along with the NetASM source package.  If not, see
# ##        http://www.gnu.org/licenses/.

__author__ = 'shahbaz'

from netasm.netasm.core import *


def main():
    # Constants
    PORT_COUNT_BITMAP = 0xFFFF  # means [... bit(1): port_2, bit(0): port_1]
    ETH_IP_TYPE = 0x0800

    # Declarations
    decls = Decls(TableDecls())

    # Tables
    # Ethernet address table
    MAC_TABLE_SIZE = Size(16)
    decls.table_decls[TableId('eth_match_table')] = \
        Table(TableFieldsCollection.MatchFields(),
            MAC_TABLE_SIZE,
            TableTypeCollection.CAM)
    match_table = decls.table_decls[TableId('eth_match_table')]
    match_table.table_fields[Field('eth_addr')] = Size(48), MatchTypeCollection.Binary

    decls.table_decls[TableId('eth_params_table')] = \
        Table(TableFieldsCollection.SimpleFields(),
            MAC_TABLE_SIZE,
            TableTypeCollection.RAM)
    params_table = decls.table_decls[TableId('eth_params_table')]
    params_table.table_fields[Field('outport_bitmap')] = Size(3)

    # Index address table
    INDEX_TABLE_SIZE = Size(1)
    decls.table_decls[TableId('index_table')] = \
        Table(TableFieldsCollection.SimpleFields(),
            INDEX_TABLE_SIZE,
            TableTypeCollection.RAM)
    index_table = decls.table_decls[TableId('index_table')]
    index_table.table_fields[Field('index')] = Size(16)

    # Add your logic here ...
    # -begin-

    # Implement the following:
    # 1. Create a new acl match table and add it in the table_decls (see above for examples)
    #    a. Table should have match field types as we will be doing an exact match on ip src and dst
    #       (see eth_match_table)
    #    b. Should be of size 16
    #    c. Should be of type CAM
    #
    # 2. Add two fields in the table for ip src and dst
    #    a. Should be of size 32 (i.e., ip field size)
    #    b. Should have a binary match type

    ACL_TABLE_SIZE = Size(16)
    decls.table_decls[TableId('acl_match_table')] = \
        Table(TableFieldsCollection.MatchFields(),
            ACL_TABLE_SIZE,
            TableTypeCollection.CAM)
    match_table = decls.table_decls[TableId('acl_match_table')]
    match_table.table_fields[Field('ipv4_src')] = Size(32), MatchTypeCollection.Binary
    match_table.table_fields[Field('ipv4_dst')] = Size(32), MatchTypeCollection.Binary

    # -end-

    # Code
    code = I.Code(
        ##################
        ### Arguments ####
        ##################
        Fields(),

        ##################
        ## Instructions ##
        ##################
        I.Instructions(
            ##################
            ## Parse packet ##
            ##################

            # Add ethernet header fields in the header set
            I.ADD(O.Field(Field('eth_dst')),
                  Size(48)),
            I.ADD(O.Field(Field('eth_src')),
                  Size(48)),
            I.ADD(O.Field(Field('eth_type')),
                  Size(16)),

            # Add you logic here ...
            # -begin-

            # Implement the following:
            # 1. Add a 1-bit field say has_ip to check if the packet was an ip packet or not
            # 2. Add ip header fields (not the size is specified in bits)

            # Add ip header fields
            I.ADD(O.Field(Field('has_ip')),
                  Size(1)),
            I.ADD(O.Field(Field('ipv4_ver')),
                  Size(4)),
            I.ADD(O.Field(Field('ipv4_ihl')),
                  Size(4)),
            I.ADD(O.Field(Field('ipv4_dscp')),
                  Size(6)),
            I.ADD(O.Field(Field('ipv4_ecn')),
                  Size(2)),
            I.ADD(O.Field(Field('ipv4_tlen')),
                  Size(16)),
            I.ADD(O.Field(Field('ipv4_id')),
                  Size(16)),
            I.ADD(O.Field(Field('ipv4_flgs')),
                  Size(3)),
            I.ADD(O.Field(Field('ipv4_fo')),
                  Size(13)),
            I.ADD(O.Field(Field('ipv4_ttl')),
                  Size(8)),
            I.ADD(O.Field(Field('ipv4_prtcl')),
                  Size(8)),
            I.ADD(O.Field(Field('ipv4_chksm')),
                  Size(16)),
            I.ADD(O.Field(Field('ipv4_src')),
                  Size(32)),
            I.ADD(O.Field(Field('ipv4_dst')),
                  Size(32)),

            # -end-

            # Load fields with default values
            I.LD(O.Field(Field('eth_dst')),
                 O.Value(Value(0, Size(48)))),
            I.LD(O.Field(Field('eth_src')),
                 O.Value(Value(0, Size(48)))),
            I.LD(O.Field(Field('eth_type')),
                 O.Value(Value(0, Size(16)))),

            # Add your logic here ...
            # -begin-

            # Load ip header fields with default value of 0

            I.LD(O.Field(Field('has_ip')),
                 O.Value(Value(0, Size(1)))),
            I.LD(O.Field(Field('ipv4_ver')),
                 O.Value(Value(0, Size(4)))),
            I.LD(O.Field(Field('ipv4_ihl')),
                 O.Value(Value(0, Size(4)))),
            I.LD(O.Field(Field('ipv4_dscp')),
                 O.Value(Value(0, Size(6)))),
            I.LD(O.Field(Field('ipv4_ecn')),
                 O.Value(Value(0, Size(2)))),
            I.LD(O.Field(Field('ipv4_tlen')),
                 O.Value(Value(0, Size(16)))),
            I.LD(O.Field(Field('ipv4_id')),
                 O.Value(Value(0, Size(16)))),
            I.LD(O.Field(Field('ipv4_flgs')),
                 O.Value(Value(0, Size(3)))),
            I.LD(O.Field(Field('ipv4_fo')),
                 O.Value(Value(0, Size(13)))),
            I.LD(O.Field(Field('ipv4_ttl')),
                 O.Value(Value(0, Size(8)))),
            I.LD(O.Field(Field('ipv4_prtcl')),
                 O.Value(Value(0, Size(8)))),
            I.LD(O.Field(Field('ipv4_chksm')),
                 O.Value(Value(0, Size(16)))),
            I.LD(O.Field(Field('ipv4_src')),
                 O.Value(Value(0, Size(32)))),
            I.LD(O.Field(Field('ipv4_dst')),
                 O.Value(Value(0, Size(32)))),

            # -end

            # Parse ethernet
            # load ethernet header fields from the packet
            I.LD(O.Field(Field('eth_dst')),
                 O.Location(
                     Location(
                         O.Value(Value(0, Size(16)))))),
            I.LD(O.Field(Field('eth_src')),
                 O.Location(
                     Location(
                         O.Value(Value(48, Size(16)))))),
            I.LD(O.Field(Field('eth_type')),
                 O.Location(
                     Location(
                         O.Value(Value(96, Size(16)))))),

            # Add your logic here ...
            # -begin-

            # Implement the following:
            # 1. Check if the incoming packet is ip (use BR instruction for this purpose)
            #    a. if not ip, load has_ip with value 0 and jump to l2 learning
            #    b. else if is ip, load has_ip with value 1 and load the ip field values from the packet

            # Check if the incoming packet has an ip header
            I.BR(O.Field(Field('eth_type')),
                 Op.Eq,
                 O.Value(Value(ETH_IP_TYPE, Size(16))),
                 Label('LBL_PARSE_0')),

            # Case: not an ip packet
            I.LD(O.Field(Field('has_ip')),
                 O.Value(Value(0, Size(1)))),
            I.JMP(Label('LBL_L2')),

            # Case: is an ip packet
            I.LBL(Label('LBL_PARSE_0')),

            # load ip header fields from the packet
            # Note: we assume that ip has no optional fields
            I.LD(O.Field(Field('has_ip')),
                 O.Value(Value(1, Size(1)))),
            I.LD(O.Field(Field('ipv4_ver')),
                 O.Location(
                     Location(
                         O.Value(Value(112, Size(16)))))),
            I.LD(O.Field(Field('ipv4_ihl')),
                 O.Location(
                     Location(
                         O.Value(Value(116, Size(16)))))),
            I.LD(O.Field(Field('ipv4_dscp')),
                 O.Location(
                     Location(
                         O.Value(Value(120, Size(16)))))),
            I.LD(O.Field(Field('ipv4_ecn')),
                 O.Location(
                     Location(
                         O.Value(Value(126, Size(16)))))),
            I.LD(O.Field(Field('ipv4_tlen')),
                 O.Location(
                     Location(
                         O.Value(Value(128, Size(16)))))),
            I.LD(O.Field(Field('ipv4_id')),
                 O.Location(
                     Location(
                         O.Value(Value(144, Size(16)))))),
            I.LD(O.Field(Field('ipv4_flgs')),
                 O.Location(
                     Location(
                         O.Value(Value(160, Size(16)))))),
            I.LD(O.Field(Field('ipv4_fo')),
                 O.Location(
                     Location(
                         O.Value(Value(163, Size(16)))))),
            I.LD(O.Field(Field('ipv4_ttl')),
                 O.Location(
                     Location(
                         O.Value(Value(176, Size(16)))))),
            I.LD(O.Field(Field('ipv4_prtcl')),
                 O.Location(
                     Location(
                         O.Value(Value(184, Size(16)))))),
            I.LD(O.Field(Field('ipv4_chksm')),
                 O.Location(
                     Location(
                         O.Value(Value(192, Size(16)))))),
            I.LD(O.Field(Field('ipv4_src')),
                 O.Location(
                     Location(
                         O.Value(Value(208, Size(16)))))),
            I.LD(O.Field(Field('ipv4_dst')),
                 O.Location(
                     Location(
                         O.Value(Value(240, Size(16)))))),

            # -end-

            #################
            ## L2 Learning ##
            #################

            I.LBL(Label('LBL_L2')),

            I.ATM(
                I.Code(
                    Fields(Field('eth_dst'), Field('eth_src')),
                    I.Instructions(
                        # Add the following header fields in the header set
                        I.ADD(O.Field(Field('index')),
                              Size(16)),

                        # Lookup in the match table and store the matched index
                        I.LKt(O.Field(Field('index')),
                              TableId('eth_match_table'),
                              O.Operands_(
                                  O.Field(Field('eth_dst')))),
                        I.BR(O.Field(Field('index')),
                             Op.Neq,
                             O.Value(Value(-1, Size(16))),
                             Label('LBL_LKP_0')),

                        # Case: there is no match in the match table
                        # Broadcast the packet
                        I.OP(
                            O.Field(Field('outport_bitmap')),
                            O.Field(Field('inport_bitmap')),
                            Op.Xor,
                            O.Value(Value(PORT_COUNT_BITMAP, Size(16))),
                        ),
                        I.JMP(Label('LBL_LRN')),

                        # Case: there is a match in the l2 match table
                        I.LBL(Label('LBL_LKP_0')),

                        # Load output port from the parameters table
                        I.LDt(
                            O.Operands__(
                                O.Field(Field('outport_bitmap'))),
                            TableId('eth_params_table'),
                            O.Field(Field('index'))),

                        #######################
                        ## Learn MAC address ##
                        #######################
                        I.LBL(Label('LBL_LRN')),

                        # Lookup in the match table and store the matched index
                        I.LKt(O.Field(Field('index')),
                              TableId('eth_match_table'),
                              O.Operands_(
                                  O.Field(Field('eth_src')))),
                        I.BR(O.Field(Field('index')),
                             Op.Neq,
                             O.Value(Value(-1, Size(16))),
                             Label('LBL_LRN_0')),

                        # Case: there is no match in the match table
                        # Read the running index from the index table
                        I.LDt(
                            O.Operands__(
                                O.Field(Field('index'))),
                            TableId('index_table'),
                            O.Value(Value(0, Size(1)))),

                        # Store eth_src in the eth_match_table
                        I.STt(TableId('eth_match_table'),
                              O.Field(Field('index')),
                              O.OperandsMasks_(
                                  (O.Field(Field('eth_src')), Mask(0xFFFFFFFFFFFF)))),

                        # Store inport_bitmap in the eth_params_table
                        I.STt(TableId('eth_params_table'),
                              O.Field(Field('index')),
                              O.Operands_(
                                  O.Field(Field('inport_bitmap')))),

                        # Increment the running index
                        I.OP(
                            O.Field(Field('index')),
                            O.Field(Field('index')),
                            Op.Add,
                            O.Value(Value(1, Size(16))),
                        ),

                        # Check if the index is less than the MAC_TABLE_SIZE
                        I.BR(O.Field(Field('index')),
                             Op.Lt,
                             O.Value(Value(MAC_TABLE_SIZE, Size(16))),
                             Label('LBL_LRN_1')),

                        # Reset the running index
                        I.LD(O.Field(Field('index')),
                             O.Value(Value(0, Size(16)))),

                        # Store the running index back in the table
                        I.LBL(Label('LBL_LRN_1')),

                        I.STt(TableId('index_table'),
                              O.Value(Value(0, Size(1))),
                              O.Operands_(
                                  O.Field(Field('index')))),
                        I.JMP(Label('LBL_HLT')),

                        # Store the current inport_bitmap in the eth_params_table
                        I.LBL(Label('LBL_LRN_0')),

                        I.STt(TableId('eth_params_table'),
                              O.Field(Field('index')),
                              O.Operands_(
                                  O.Field(Field('inport_bitmap')))),

                        # Halt
                        I.LBL(Label('LBL_HLT')),
                        I.HLT()
                    )
                )
            ),

            #########
            ## ACL ##
            #########

            I.LBL(Label('LBL_ACL')),

            # Add your logic here ...
            # -begin-

            # Implement the following:
            # 1. Check if the packet is ip using has_ip field
            #    a. if not ip, jump to the HLT instruction
            #    b. else if is ip, lookup in the acl match table (see eth_match_table lookup example above)
            #       1. if no match, drop the packet (you can use the DRP instruction here, but remember to jump to the
            #          HLT instruction
            #       2. else pass through (you can use the ID instruction for this)

            I.BR(O.Field(Field('has_ip')),
                 Op.Eq,
                 O.Value(Value(1, Size(16))),
                 Label('LBL_ACL_0')),

            # Case: not an ip packet (do nothing)
            I.ID(),
            I.JMP(Label('LBL_HLT')),

            # Case: is an ip packet
            I.LBL(Label('LBL_ACL_0')),

            # Add acl_index header field
            I.ADD(O.Field(Field('acl_index')),
                  Size(16)),

            # Lookup in the acl match table and store the matched index
            I.LKt(O.Field(Field('acl_index')),
                  TableId('acl_match_table'),
                  O.Operands_(
                      O.Field(Field('ipv4_src')),
                      O.Field(Field('ipv4_dst')))),
            I.BR(O.Field(Field('acl_index')),
                 Op.Neq,
                 O.Value(Value(-1, Size(16))),
                 Label('LBL_ACL_1')),

            # Case: no match in the acl table
            I.DRP(Reason('no match in the acl table', '')),
            I.JMP(Label('LBL_HLT')),

            # Case: match in the acl table
            I.LBL(Label('LBL_ACL_1')),

            # Pass through
            I.ID(),

            # -end-

            ##########
            ## Halt ##
            ##########
            I.LBL(Label('LBL_HLT')),
            I.HLT()
        )
    )

    return Policy(decls, code)

# Testing
if __name__ == "__main__":
    policy = main()

    # Cost
    if True:
        from netasm.netasm import cost
        area, latency = cost.cost_Policy(policy)
        print area, latency

    # Execute
    if False:
        from netasm.netasm import execute

        policy = execute.Execute(policy)

        state = execute.State(execute.Header(), execute.Packet(1000))
        # Add special fields (see netasm/core/common.py)
        state.header[Field('inport_bitmap')] = Value(0, Size(64))
        state.header[Field('outport_bitmap')] = Value(0, Size(64))
        state.header[Field('bit_length')] = Value(len(state.packet), Size(64))
        state.header[Field('DRP')] = Value(0, Size(1))
        state.header[Field('CTR')] = Value(0, Size(1))

        policy.start()

        from netasm.netasm.core.utilities.profile import time_usage

        @time_usage
        def run():
            iterations = 10

            for i in range(iterations):
                policy.put(state)

            for i in range(iterations):
                policy.get()

        run()

        policy.stop()
